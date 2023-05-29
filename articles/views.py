from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions, viewsets

from articles.models import Article, Comment
from articles.serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    ArticleUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)


class ArticlesPaginationViewSet(viewsets.ModelViewSet):
    """
    페이지네이션
    """
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination


# articles/
class ArticleView(APIView):
    # 로그인한 사람은 게시글 작성 가능. 아니면 게시글 전체 목록 조회만 가능.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    게시글 전체 목록 조회
    """

    def get(self, request):
        articles = Article.objects.all().order_by("-created_at")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 작성
    """

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(({"message": "게시글 작성 완료!"}, serializer.data), status=status.HTTP_201_CREATED)


# articles/<int:article_id>/
class ArticleDetailView(APIView):
    # 로그인한 사람은 게시글 수정/삭제 가능. 아니면 게시글 상세보기만 가능.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    게시글 상세보기
    """

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 수정하기
    """

    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleUpdateSerializer(article, data=request.data)
        if article.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(({"message": "게시글 수정 완료!"},serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    """
    게시글 삭제하기
    """

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.user == request.user:
            article.delete()
            return Response({"message": "게시글 삭제 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# articles/<int:article_id>/comments/
class CommentView(APIView):
    # 로그인한 사람은 댓글 작성 가능. 아니면 댓글 조회만 가능.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    댓글 조회
    """

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comments = article.comments.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    댓글 작성
    """

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, user=request.user)
            return Response(({"message": "댓글 작성 완료!"}, serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# articles/comments/<int:comment_id>/
class CommentDetailView(APIView):
    # 로그인한 사람만 댓글 수정/삭제 가능
    permission_classes = [permissions.IsAuthenticated]
    """
    댓글 수정
    """

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentCreateSerializer(comment, data=request.data)
        if comment.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(({"message": "댓글 수정 완료!"}, serializer.data), status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    """
    댓글 삭제
    """

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response({"message": "댓글 삭제 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# articles/<int:article_id>/like/
class LikeView(APIView):
    # 로그인한 사람만 좋아요 가능
    permission_classes = [permissions.IsAuthenticated]
    """
    게시글 좋아요
    """

    def post(self, request, article_id):
        article = get_object_or_404(Article, id = article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message":"좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message":"좋아요"}, status=status.HTTP_200_OK)
