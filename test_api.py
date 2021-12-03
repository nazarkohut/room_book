import unittest

import requests
from flask_testing import TestCase

from app import app, db
from misc.db_misc import engine, session
from model.table.apartment import Apartment
from model.table.city import City
from model.table.famous_place import FamousPlace
from model.table.hotel import Hotel
from model.table.reserve import Reserve
from model.table.user import User


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{username}:{password}@{server}/room_book_db"
        return app


url = 'http://127.0.0.1:5000'


class Test(BaseTestCase):
    # def test_register_admin(self):
    #     # you have to manually set is_admin to 1
    #     self.assert_200(self.client.post('/registration',
    #                                      json={
    #                                          "email": "admin1@example.com",
    #                                          "username": "admin1",
    #                                          "password": "admin1_password",
    #                                          "birthday": "2003-06-02",
    #                                          "hotel_owner": False
    #                                      }))  # register as admin

    def test_Aregister(self):
        self.assert_200(self.client.post('/registration',
                                         json={
                                             "email": "user1@example.com",
                                             "username": "user1",
                                             "password": "user1_password",
                                             "birthday": "2003-06-02",
                                             "hotel_owner": False
                                         }))  # register as user

        self.assert_200(self.client.post('/registration',
                                         json={
                                             "email": "user2@example.com",
                                             "username": "user2",
                                             "password": "user2_password",
                                             "birthday": "2003-06-02",
                                             "hotel_owner": True
                                         }))  # register as hotel_owner

        self.assert_400(self.client.post('/registration',
                                         json={
                                             "email": "user1@example.com",
                                             "username": "user1",
                                             "password": "user1_password",
                                             "birthday": "2003-06-02",
                                             "hotel_owner": False
                                         }))  # register as user

        self.assert_400(self.client.post('/registration',
                                         json={
                                             "email": "user2@example.com",
                                             "username": "user2",
                                             "password": "user2_password",
                                             "birthday": "2003-06-02",
                                             "hotel_owner": True
                                         }))  # register as hotel_owner

    def login_as_admin(self):
        res = requests.post(url + '/login', json={"email": "admin1@example.com",
                                                  "password": "admin1_password"
                                                  })
        access_token = res.json()["access_token"]
        admin_credentials = 'YWRtaW4xQGV4YW1wbGUuY29tOmFkbWluMV9wYXNzd29yZA=='
        return access_token, admin_credentials

    def login_as_hotel_owner(self):
        res = requests.post(url + '/login', json={
            "email": "user2@example.com",
            "password": "user2_password"
        })
        access_token = res.json()["access_token"]
        return access_token

    def login_as_user(self):
        res = requests.post(url + '/login', json={
            "email": "user1@example.com",
            "password": "user1_password"
        })
        access_token = res.json()["access_token"]
        return access_token

    def test_Buser(self):
        print("USER")
        access_token, admin_credentials = self.login_as_admin()

        # get
        self.assert_200(self.client.get('/profile/1',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

        # logout
        self.assert_200(
            self.client.post('/logout', headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

    def test_Ccity(self):
        print("CITY")
        access_token, admin_credentials = self.login_as_admin()
        #  post
        self.assert_200(
            self.client.post('/city', headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                             json={
                                 "city": "string15",
                                 "city_image": "string",
                                 "country": "string",
                                 "population": 0
                             }))  # got through two levels of authorization (admin only)
        city_id = session.query(City).filter(City.city == "string15").first().id
        # get
        self.assert200(self.client.get('/city/all'))

        self.assert405(self.client.get(f'/city/{city_id}'))  # method not allowed

        # put
        self.assert_200(
            self.client.put(f'/city/{city_id}',
                            headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                            json={
                                "city": "string15",
                                "city_image": "string151511515",
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
            self.client.put(f'/city/{city_id}', headers={},
                            json={
                                "city": "string",
                                "city_image": "string",
                                "country": "string",
                                "population": 0
                            }))

        # access denied:
        self.assert_401(self.client.post('/city', headers={}, json={
            "city": "string15",
            "city_image": "string",
            "country": "string",
            "population": 0
        }))

        self.assert_401(self.client.put(f'/city/{city_id}', headers={}, json={
            "city": "string15",
            "city_image": "Imagine this is url for image.",
            "country": "string",
            "population": 0
        }))
        self.assert_401(self.client.delete(f'/city/{city_id}', headers={}))

    def test_Dfamous_place(self):
        print("FAMOUS_PLACE")
        access_token, admin_credentials = self.login_as_admin()
        city_id = session.query(City).filter(City.city == "string15").first().id

        # post
        self.assert_200(self.client.post(f'/famous_place/{city_id}',
                                         headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                         json={
                                             "famous_place": "string",
                                             "famous_place_image": "string",
                                             "entrance_fee": 100
                                         }
                                         ))

        self.assert_401(self.client.post(f'/famous_place/{city_id}',
                                         headers={'Authorization': f'Bearer {self.login_as_user()}'},
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
        famous_place_id = session.query(FamousPlace).filter(FamousPlace.famous_place == "string").first().id

        self.assert_200(self.client.get(f'/famous_place/{city_id}',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        ))

        self.assert_404(self.client.get('/famous_place/6000',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        ))

        # put
        self.assert_200(self.client.put(f'/particular_famous_place/{famous_place_id}',
                                        headers={'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'},
                                        json={
                                            "city_id": city_id,
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

    def test_Ehotel(self):
        print("HOTEL")
        city_id = session.query(City).filter(City.city == "string15").first().id
        # post
        self.assert_200(
            self.client.post(f'hotel/{city_id}', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                             json={
                                 "hotel": "string",
                                 "stars": 5,
                                 "image_link": "string",
                                 "description": "string"}
                             ))
        self.assert_403(
            self.client.post(f'hotel/{city_id}', headers={'Authorization': f'Bearer {self.login_as_user()}'},
                             json={
                                 "hotel": "string",
                                 "stars": 5,
                                 "image_link": "string",
                                 "description": "string"}
                             ))

        # get
        # in city
        self.assert_200(
            self.client.get(f'/hotels/{city_id}', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_404(
            self.client.get('/hotels/600', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))
        hotel_id = session.query(Hotel).filter(Hotel.hotel == "string").first().id
        # particular hotel
        self.assert_200(
            self.client.get(f'/hotel/{hotel_id}', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_404(
            self.client.get('/hotel/600', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        # put
        self.assert_200(
            self.client.put(f'/hotel/{hotel_id}', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={
                                "city_id": city_id,
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"
                            }
                            ))

        self.assert_404(
            self.client.put('/hotel/600', headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={
                                "city_id": 2,
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

        self.assert_403(
            self.client.put(f'/hotel/{hotel_id}', headers={'Authorization': f'Bearer {self.login_as_user()}'},
                            json={
                                "city_id": 2,
                                "hotel": "string",
                                "stars": 5,
                                "image_link": "string",
                                "description": "string"}
                            ))

    def test_Fapartment(self):
        print("APARTAMENT")
        hotel_id = session.query(Hotel).filter(Hotel.hotel == "string").first().id
        # post
        self.assert_200(
            self.client.post(f'/apartment/{hotel_id}',
                             headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                             json={"image": "string",
                                   "is_available": True,
                                   "room_capacity": 0,
                                   "floor": 0,
                                   "cost": 0,
                                   "description": "string"
                                   }))
        self.assert_403(
            self.client.post(f'/apartment/{hotel_id}', headers={'Authorization': f'Bearer {self.login_as_user()}'},
                             json={"image": "string",
                                   "is_available": True,
                                   "room_capacity": 0,
                                   "floor": 0,
                                   "cost": 0
                                   }))

        # get
        self.assert_200(self.client.get(f'/apartment/{hotel_id}'))
        self.assert_404(self.client.get('/apartment/500'))

        apartament_id = session.query(Apartment).filter(Apartment.image == "string").first().id

        self.assert_200(self.client.get(f'/particular_apartment/{apartament_id}'))
        self.assert_404(self.client.get('/particular_apartment/500'))

        # put
        self.assert_200(
            self.client.put(f'/particular_apartment/{apartament_id}',
                            headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                            json={"image": "string",
                                  "is_available": True,
                                  "room_capacity": 0,
                                  "floor": 0,
                                  "cost": 0,
                                  "description": "string"
                                  }))

        self.assert_403(
            self.client.put(f'/particular_apartment/{apartament_id}',
                            headers={'Authorization': f'Bearer {self.login_as_user()}'},
                            json={"image": "string",
                                  "is_available": True,
                                  "room_capacity": 0,
                                  "floor": 0,
                                  "cost": 0
                                  }))

    def test_Greserve(self):
        print("RESERVE")
        apartament_id = session.query(Apartment).filter(Apartment.image == "string").first().id
        self.assert_200(
            self.client.post(f'/reserve/{apartament_id}',
                             headers={'Authorization': f'Bearer {self.login_as_user()}'},
                             json={
                                 "reserve_start_date": "2021-07-21",
                                 "reserve_finish_date": "2021-08-22"
                             }))
        self.assert_400(
            self.client.post(f'/reserve/{apartament_id}',
                             headers={'Authorization': f'Bearer {self.login_as_user()}'},
                             json={
                                 "reserve_start_date": "2021-08-22",
                                 "reserve_finish_date": "2021-06-22"
                             }))
        self.assert_403(
            self.client.post(f'/reserve/{apartament_id}',
                             headers={'Authorization': f'Bearer {self.login_as_hotel_owner()}'},
                             json={
                                 "reserve_start_date": "2021-05-22",
                                 "reserve_finish_date": "2021-08-22"
                             }))

        self.assert_200(
            self.client.get(f'/reserve/{apartament_id}',
                            headers={'Authorization': f'Bearer {self.login_as_user()}'}))
        reserve_id = session.query(Reserve).filter(Reserve.reserve_start_date == "2021-07-21").first().id

        assert self.client.get(f'/reserve/{apartament_id}',
                               headers={'Authorization': f'Bearer {self.login_as_user()}'}).json == [{'id': reserve_id,
                                                                                                       'reserve_cost': None,
                                                                                                       'reserve_finish_date': 'Sun, 22 Aug 2021 00:00:00 GMT',
                                                                                                       'reserve_id': apartament_id,
                                                                                                       'reserve_start_date': 'Wed, 21 Jul 2021 00:00:00 GMT',
                                                                                                       'user_id': None}]

    def test_Hdelete(self):
        print("DELETE")
        access_token, admin_credentials = self.login_as_admin()

        famous_place_id = session.query(FamousPlace).filter(FamousPlace.famous_place == "string").first().id
        reserve_id = session.query(Reserve).filter(Reserve.reserve_start_date == "2021-07-21").first().id
        apartament_id = session.query(Apartment).filter(Apartment.image == "string").first().id
        hotel_id = session.query(Hotel).filter(Hotel.hotel == "string").first().id
        city_id = session.query(City).filter(City.city == "string15").first().id

        self.assert_200(self.client.delete(f'/particular_famous_place/{famous_place_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))
        self.assert_404(self.client.delete(f'/particular_famous_place/{famous_place_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

        self.assert_200(
            self.client.delete(f'/reserve/{reserve_id}',
                               headers={'Authorization': f'Bearer {self.login_as_user()}'}))

        self.assert_400(
            self.client.delete(f'/reserve/{reserve_id}',
                               headers={'Authorization': f'Bearer {self.login_as_user()}'}))

        self.assert_200(self.client.delete(f'/particular_apartment/{apartament_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))
        self.assert_400(self.client.delete(f'/particular_apartment/{apartament_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

        self.assert_200(self.client.delete(f'/hotel/{hotel_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))
        self.assert_404(self.client.delete(f'/hotel/{hotel_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

        self.assert_200(self.client.delete(f'/city/{city_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))
        self.assert_404(self.client.delete(f'/city/{city_id}', headers={
            'Authorization': f'Basic {admin_credentials}, Bearer {access_token}'}))

        user1 = session.query(User).filter((User.username == "user1")).first()
        user2 = session.query(User).filter((User.username == "user2")).first()

        session.delete(user1)
        session.delete(user2)
        session.commit()


if __name__ == '__main__':
    unittest.main()
