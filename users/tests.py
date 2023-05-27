from rest_framework.test import APITestCase

from .models import User
from django.urls import reverse


# 마이페이지 출력 테스트
class MyPageTest(APITestCase):
    def setUp(self):
        self.user_data = {"email": "aaa@aaa.com", "password": "aaa112!"}
        self.user = User.objects.create_user("aaa@aaa.com", "aaa112!")
        
    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        response = self.client.get(
            path=reverse("mypage"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.user_data['email'])


# 유저페이지 출력 테스트
class UserPageTest(APITestCase):
    def setUp(self):
        # 유저 1 생성
        self.user_data = {"email": "aaa@aaa.com", "password": "aaa112!"}
        self.user = User.objects.create_user("aaa@aaa.com", "aaa112!")      

        # 유저 2 생성
        self.user_data2 = {"email": "bbb@bbb.com", "password": "bbb!"}
        self.user2 = User.objects.create(email="bbb@bbb.com", password="bbb!", nickname="bbb")
        self.user2.set_password("password")        
        self.user2.save()


    # 본인 페이지 출력 테스트 
    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user.id
        url = reverse("user_view", kwargs={"user_id": user_id})
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.user_data['email'])


    # 타인 페이지 출력 테스트
    def test_get_other_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user2.id
        url = reverse("user_view", kwargs={"user_id": user_id})
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['email'], self.user_data['email'])


# 유저 페이지 수정 테스트
class UserPageEditTest(APITestCase):
    def setUp(self):
        # 유저 1 생성
        self.user_data = {"email": "aaa@aaa.com", "password": "aaa112!"}
        self.user = User.objects.create_user("aaa@aaa.com", "aaa112!")

        # 유저 2 생성
        self.user_data2 = {"email": "bbb@bbb.com", "password": "bbb!"}
        self.user2 = User.objects.create(email="bbb@bbb.com", password="bbb!", nickname="bbb")
        self.user2.set_password("password")
        self.user2.save()


    # 본인 유저 페이지 수정
    def test_edit_user(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user.id
        url = reverse("user_view", kwargs={"user_id": user_id})
        response = self.client.put(
            path=url,
            data = {
                "nickname":"edit_aaa",
                "bio":"edit_bio_aaa",
                "image":"edit_image_url_aaa"
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)
        
    # 타인 유저 페이지 수정
    def test_edit_other_user(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user2.id
        url = reverse("user_view", kwargs={"user_id": user_id})
        response = self.client.put(
            path=url,
            data = {
                "nickname":"edit_bbb",
                "bio":"edit_bio_bbb",
                "image":"edit_image_url_bbb"
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 403)


    # 타인 유저 탈퇴
    def test_delete_other_user(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user2.id
        url = reverse("user_view", kwargs={"user_id": user_id})
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 403)


    # 본인 계정 탈퇴 
    def test_delete_user(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user.id
        url = reverse("user_view", kwargs={"user_id": user_id})
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)


class UserFolloweTest(APITestCase):
    def setUp(self):
        # 유저 1 생성
        self.user_data = {"email": "aaa@aaa.com", "password": "aaa112!"}
        self.user = User.objects.create_user("aaa@aaa.com", "aaa112!")

        # 유저 2 생성
        self.user_data2 = {"email": "bbb@bbb.com", "password": "bbb!"}
        self.user2 = User.objects.create(email="bbb@bbb.com", password="bbb!", nickname="bbb")
        self.user2.set_password("password")        
        self.user2.save()


    # 본인 팔로우 불가
    def test_follow_self(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user.id
        url = reverse("follow_view", kwargs={"user_id": user_id})
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 403)


    # 타인 팔로우 확인
    def test_follow_self(self):
        # 팔로우 확인
        access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        user_id = self.user2.id
        url = reverse("follow_view", kwargs={"user_id": user_id})
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)


