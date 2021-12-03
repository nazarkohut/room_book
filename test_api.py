import unittest

import requests
from flask_testing import TestCase
from app import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{username}:{password}@{server}/room_book_db"
        return app


url = 'http://127.0.0.1:5000'


class Test(BaseTestCase):

    def test_login_as_admin(self):
        res = requests.post(url + '/login', json={"email": "admin1@example.com",
                                                  "password": "admin1_password"
                                                  })

        access_token = res.json()["access_token"]
        admin_credentials = 'YWRtaW4xQGV4YW1wbGUuY29tOmFkbWluMV9wYXNzd29yZA=='
        return access_token, admin_credentials

    def test_login_as_hotel_owner(self):
        res = requests.post(url + '/login', json={
            "email": "user2@example.com",
            "password": "user2_password"
        })

        access_token = res.json()["access_token"]
        return access_token

    def test_login_as_user(self):
        res = requests.post(url + '/login', json={
            "email": "user1@example.com",
            "password": "user1_password"
        })

        access_token = res.json()["access_token"]
        return access_token

    # def test_register(self):
    #     self.assert_200(self.client.post('/registration',
    #                                      json={
    #                                          "email": "user1@example.com",
    #                                          "username": "user1",
    #                                          "password": "user1_password",
    #                                          "birthday": "2003-06-02",
    #                                          "hotel_owner": "False"
    #                                      }))  # register as user
    #
    #     self.assert_200(self.client.post('/registration',
    #                                      json={
    #                                          "email": "admin1@example.com",
    #                                          "username": "admin1",
    #                                          "password": "admin1_password",
    #                                          "birthday": "2003-06-02",
    #                                          "hotel_owner": "False"
    #                                      }))  # register as admin
    #
    #     self.assert_200(self.client.post('/registration',
    #                                      json={
    #                                          "email": "user2@example.com",
    #                                          "username": "user2",
    #                                          "password": "user2_password",
    #                                          "birthday": "2003-06-02",
    #                                          "hotel_owner": "True"
    #                                      }))  # register as hotel_owner

    def test_user(self):
        access_token, admin_credentials = self.test_login_as_admin()

        # get
        self.assert_200(self.client.get('/profile/5',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

        # logout
        self.assert_200(
            self.client.post('/logout', headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))



    def test_city(self):
        # access denied:
        access_token, admin_credentials = self.test_login_as_admin()
        self.assert_401(self.client.post('/city', headers={}, json={
            "city": "string15",
            "city_image": "string",
            "country": "string",
            "population": 0
        }))
        self.assert_401(self.client.put('/city/5', headers={}, json={
            "city": "string15",
            "city_image": "Imagine this is url for image.",
            "country": "string",
            "population": 0
        }))
        self.assert_401(self.client.delete('/city/5', headers={}))
        #  post
        self.assert_200(
            self.client.post('/city', headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                             json={
                                 "city": "string15",
                                 "city_image": "string",
                                 "country": "string",
                                 "population": 0
                             }))  # got through two levels of authorization (admin only)

        self.assert_401(
            self.client.post('/city', headers={},
                             json={
                                 "city": "string15",
                                 "city_image": "string",
                                 "country": "string",
                                 "population": 0
                             }))  # got through two levels of authorization (admin only)

        # get
        self.assert200(self.client.get('/city/all'))
        self.assert405(self.client.get('/city/2'))  # method not allowed

        # put
        self.assert_200(
            self.client.put('/city/5', headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                            json={
                                "city": "string",
                                "city_image": "string",
                                "country": "string",
                                "population": 0
                            }))  # got through two levels of authorization (admin only)

        self.assert_404(
            self.client.put('/city/500', headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                            json={
                                "city": "string",
                                "city_image": "string",
                                "country": "string",
                                "population": 0
                            }))  # got through two levels of authorization (admin only)

        self.assert_401(
            self.client.put('/city/500', headers={},
                            json={
                                "city": "string",
                                "city_image": "string",
                                "country": "string",
                                "population": 0
                            }))

    def test_famous_place(self):
        access_token, admin_credentials = self.test_login_as_admin()
        # post
        self.assert_200(self.client.post('/famous_place/2',
                                         headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                         json={
                                             "famous_place": "string",
                                             "famous_place_image": "string",
                                             "entrance_fee": 100
                                         }
                                         ))

        self.assert_401(self.client.post('/famous_place/2',
                                         headers={'Authorization': f'Bearer {self.test_login_as_user()}'},
                                         json={
                                             "famous_place": "string",
                                             "famous_place_image": "string",
                                             "entrance_fee": 100
                                         }
                                         ))

        self.assert_404(self.client.post('/famous_place/6000',
                                         headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                         json={
                                             "famous_place": "string",
                                             "famous_place_image": "string",
                                             "entrance_fee": 100
                                         }
                                         ))

        # get

        self.assert_200(self.client.get('/famous_place/2',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        ))

        self.assert_404(self.client.get('/famous_place/6000',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        ))

        # put
        self.assert_200(self.client.put('/particular_famous_place/3',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        json={
                                            "city_id": 6,
                                            "famous_place": "string",
                                            "famous_place_image": "string",
                                            "entrance_fee": 100
                                        }))

        self.assert_404(self.client.put('/particular_famous_place/60000',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        json={
                                            "city_id": 6,
                                            "famous_place": "string",
                                            "famous_place_image": "string",
                                            "entrance_fee": 100
                                        }))

    def test_hotel(self):
        # post
        self.assert_200(
            self.client.post('hotel/2', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                             json={
                                 "hotel": "string",
                                 "stars": 5,
                                 "image_link": "string",
                                 "description": "string"}
                             ))
        self.assert_403(
            self.client.post('hotel/2', headers={'Authorization': f'Bearer {self.test_login_as_user()}'},
                             json={
                                 "hotel": "string",
                                 "stars": 5,
                                 "image_link": "string",
                                 "description": "string"}
                             ))

        # get
        # in city
        self.assert_200(
            self.client.get('/hotels/2', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_404(
            self.client.get('/hotels/600', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        # particular hotel
        self.assert_200(
            self.client.get('/hotel/2', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_404(
            self.client.get('/hotel/600', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        # put
        self.assert_200(
            self.client.put('/hotel/2', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={
                                "city_id": 2,
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_404(
            self.client.put('/hotel/600', headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={
                                "city_id": 2,
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_403(
            self.client.put('/hotel/600', headers={'Authorization': f'Bearer {self.test_login_as_user()}'},
                            json={
                                "city_id": 2,
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

    def test_apartment(self):
        # post
        self.assert_200(
            self.client.post('/apartment/2',
                             headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                             json={"image": "string",
                                   "is_available": True,
                                   "room_capacity": 0,
                                   "floor": 0,
                                   "cost": 0,
                                   "description": "string"
                                   }))
        self.assert_403(
            self.client.post('/apartment/2', headers={'Authorization': f'Bearer {self.test_login_as_user()}'},
                             json={"image": "string",
                                   "is_available": True,
                                   "room_capacity": 0,
                                   "floor": 0,
                                   "cost": 0
                                   }))

        # get
        self.assert_200(self.client.get('/apartment/2'))
        self.assert_404(self.client.get('/apartment/500'))

        self.assert_200(self.client.get('/particular_apartment/3'))
        self.assert_404(self.client.get('/particular_apartment/500'))

        # put
        self.assert_200(
            self.client.put('/particular_apartment/3',
                            headers={'Authorization': f'Bearer {self.test_login_as_hotel_owner()}'},
                            json={"image": "string",
                                  "is_available": True,
                                  "room_capacity": 0,
                                  "floor": 0,
                                  "cost": 0,
                                  "description": "string"
                                  }))

        self.assert_403(
            self.client.put('/particular_apartment/3',
                            headers={'Authorization': f'Bearer {self.test_login_as_user()}'},
                            json={"image": "string",
                                  "is_available": True,
                                  "room_capacity": 0,
                                  "floor": 0,
                                  "cost": 0
                                  }))
        # self.assert_200(self.client.put('/city/5', headers={}, json={
        #     "city": "string15",
        #     "city_image": "Imagine this is url for image.",
        #     "country": "string",
        #     "population": 0
        # }))
        # self.assert_401(self.client.delete('/city/5', headers={}))
    # def test_drop(self):


if __name__ == '__main__':
    unittest.main()
