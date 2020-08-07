from django.test import TestCase
from .models import Post, User, Follow, Like
from datetime import datetime

# Create your tests here.
dt = datetime.now()
d = dt.date()
t = dt.strftime("%H:%M:%S")

class ModelsTestCase(TestCase):

    def setUp(self):
        # Create users
        u1 = User.objects.create(username="Becky")
        u2 = User.objects.create(username="Greg")
        u3 = User.objects.create(username="Fred")

        # Create posts
        p1 = Post.objects.create(user=u1, post="Hey, there", date=d, time=t)
        p2 = Post.objects.create(user=u2, post="Mi amor", date=d, time=t)
        p3 = Post.objects.create(user=u3, post="Broski", date=d, time=t)

        # Create follows
        Follow.objects.create(follow=u1, followee=u2)
        Follow.objects.create(follow=u3, followee=u1)
        Follow.objects.create(follow=u2, followee=u3)
        Follow.objects.create(follow=u1, followee=u3)


        Like.objects.create(user=u1, post=p1, like=1)
        Like.objects.create(user=u2, post=p1, like=1)
        Like.objects.create(user=u1, post=p3, like=1)


    def test_users_count(self):
        u = User.objects.all()
        self.assertEqual(u.count(), 3)

    def test_posts_count(self):
        p = Post.objects.all()
        self.assertEqual(p.count(), 3)

    def test_posters(self):
        p = Post.objects.all()
        self.assertEqual(p.count(), 3)

    def test_followers(self):
        u = User.objects.get(username="Becky")
        self.assertEqual(u.followers.count(), 1)

    def test_following(self):
        u = User.objects.get(username="Becky")
        self.assertEqual(u.following.count(), 2)

    def test_invalid_follow(self):
        u = User.objects.get(username="Becky")
        f = Follow.objects.create(follow=u, followee=u)
        self.assertFalse(f.is_valid_follow())

    def test_valid_follow(self):
        u1 = User.objects.get(username="Becky")
        u2 = User.objects.get(username="Greg")
        f = Follow.objects.create(follow=u1, followee=u2)
        self.assertTrue(f.is_valid_follow())

    def test_like(self):
        p = Post.objects.get(pk=1)
        print(p.likes.all())
        self.assertEqual(p.likes.count(), 2)