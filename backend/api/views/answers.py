from threading import Thread

from rest_framework.decorators import detail_route
from rest_framework.filters import SearchFilter

from api.models import Answer, Message
from api.serializers import AnswerSerializer, CommentSerializer, AnswerCreateSerializer
from utils.heat import HeatQueue
from utils.views import error, success, GenericViewSet
from utils import mixins


class AnswerViewSet(GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
    filter_backends = (SearchFilter,)
    search_fields = ('detail',)

    queryset = Answer.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerCreateSerializer
        if self.action == 'get_comments':
            return CommentSerializer
        return AnswerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.userSummary = self.request.user.profile
            instance.comment_count = instance.comments.count()
            serializer = self.get_serializer(instance)
            return success(serializer.data)
        return error('cant found')

    @detail_route(methods=['GET'])
    def get_comments(self, request, pk=None):
        answer = self.get_object()
        if answer is None:
            return error("no topic found")

        queryset = self.filter_queryset(answer.comments.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            for comment in page:
                profile = comment.author.profile
                comment.userSummary = profile
            serializer = self.get_serializer(page, many=True)
            temp = self.get_paginated_response(serializer.data)
            return success(temp.data)
        return error('no more data')

    def perform_create(self, serializer):
        user = self.request.user
        question = serializer.validated_data['question']
        answer = serializer.save(author=user)
        thread = Thread(target=msg_thread, args=(question, user, answer))
        thread.start()

    # TODO add auth
    @detail_route(methods=['GET'])
    def agree(self, request, pk=None):
        profile = request.user.profile
        answer = self.get_object()
        if answer is None:
            return error('no answer found')
        answer.approve += 1
        answer.save()
        profile.agreed.add(answer)
        profile.save()
        return success()

    @detail_route(methods=['GET'])
    def cancel_agree(self, request, pk=None):
        profile = request.user.profile
        answer = self.get_object()
        if answer is None:
            return error('no answer found')
        answer.approve -= 1
        answer.save()
        profile.agreed.remove(answer)
        profile.save()
        return success()

    @detail_route(methods=['GET'])
    def disagree(self, request, pk=None):
        profile = request.user.profile
        answer = self.get_object()
        if answer is None:
            return error('no answer found')
        answer.against += 1
        answer.save()
        profile.disagreed.add(answer)
        profile.save()
        return success()

    @detail_route(methods=['GET'])
    def cancel_disagree(self, request, pk=None):
        profile = request.user.profile
        answer = self.get_object()
        if answer is None:
            return error('no answer found')
        answer.against -= 1
        answer.save()
        profile.disagreed.remove(answer)
        profile.save()
        return success()

    @detail_route(methods=['GET'])
    def favorite(self, request, pk=None):
        profile = request.user.profile
        answer = self.get_object()
        if answer is None:
            return error('no answer found')
        profile.favorites.add(answer)
        profile.save()
        return success()

    @detail_route(methods=['GET'])
    def cancel_favorite(self, request, pk=None):
        profile = request.user.profile
        answer = self.get_object()
        if answer is None:
            return error('no answer found')
        profile.favorites.remove(answer)
        profile.save()
        return success()


def addMessageForUser(rec, question, answer, author):
    message = Message.objects.create(receiver=rec,
                                     question=question,
                                     answer=answer,
                                     author=author)
    message.save()
    return True


def msg_thread(question, user, answer):
    q_users = question.watchedUser.all()
    u_users = user.watchedBy.all()

    users = q_users | u_users  # merge
    for rec in users:
        receiver = rec.user
        addMessageForUser(receiver, question, answer, user)
    for topic in question.topics.all():
        HeatQueue.put(topic)