from datetime import datetime
from fastapi import status as STATUS
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List, Union

from sqlalchemy.exc import IntegrityError

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.schemas.contacts import *
from bandbase.schemas.database import *
from bandbase.schemas.forms import *


router = APIRouter(prefix='/contact', tags=['forms', 'contacts'])


@router.post('/create', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                        response_model=Acknowledgment)
def create(data: ContactData, logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    try:

        with bandbase.core.database.session() as db:

            contact = Contact()

            contact.FirstName = data.name.first
            contact.LastName = data.name.last
            contact.FullLastName = data.name.full

            contact.Street = data.address.street
            contact.HouseNumber = data.address.house
            contact.City = data.address.city
            contact.PostalCode = data.address.zip
            contact.Country = data.address.country

            contact.LandlinePhone = data.details.phone.landline
            contact.MobilePhone = data.details.phone.mobile
            contact.Fax = data.details.fax
            contact.EMail = data.details.email
            contact.WWW = data.details.website

            contact.Latitude = float(data.geopoint.latitude) \
                               if data.geopoint.latitude else None
            contact.Longitude = float(data.geopoint.longitude) \
                                if data.geopoint.longitude else None

            contact.BirthDate = datetime.strptime(data.birthdate, '%d.%m.%Y') \
                                if data.birthdate else None
            contact.CategoryID = int(data.category)
            contact.Comment = data.comment

            name = str(contact)

            logger.info(f'Creating contact "{name}"')

            db.add(contact)
            db.commit()

            id = int(contact)

            return {'id': id, 'name': name}

    except HTTPException as e:
        raise e

    except Exception as e:

        logger.exception(e)
        db.rollback()

        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to create contact: {e}')


@router.post('/read/{id}', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                           response_model=ContactData)
def read(id: int, logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    try:

        with bandbase.core.database.session() as db:

            contact = db.query(Contact).get(id)

            if not contact:

                raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND,
                                    detail=f'Unable to read contact {id}, it doesn\'t exist!')

            return {
                'name': {
                    'first': contact.FirstName,
                    'last': contact.LastName,
                    'full': contact.FullLastName
                },
                'address': {
                    'street': contact.Street,
                    'house': contact.HouseNumber,
                    'city': contact.City,
                    'zip': contact.PostalCode,
                    'country': contact.Country
                },
                'details': {
                    'phone': {
                        'landline': contact.LandlinePhone,
                        'mobile': contact.MobilePhone
                    },
                    'fax': contact.Fax,
                    'email': contact.EMail,
                    'website': contact.WWW
                    },
                'geopoint': {
                    'latitude': contact.Latitude,
                    'longitude': contact.Longitude
                },
                'birthdate': contact.BirthDate.strftime('%d.%m.%Y') if contact.BirthDate else None,
                'category': contact.CategoryID,
                'comment': contact.Comment
            }

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to read contact {id}: {e}')


@router.post('/update/{id}', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                             response_model=Acknowledgment)
def update(id: int, data: ContactData, logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    try:

        with bandbase.core.database.session() as db:

            contact = db.query(Contact).get(id)

            if not contact:

                raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND,
                                    detail=f'Unable to update contact {id}, it doesn\'t exist!')

            contact.FirstName = data.name.first
            contact.LastName = data.name.last
            contact.FullLastName = data.name.full

            contact.Street = data.address.street
            contact.HouseNumber = data.address.house
            contact.City = data.address.city
            contact.PostalCode = data.address.zip
            contact.Country = data.address.country

            contact.LandlinePhone = data.details.phone.landline
            contact.MobilePhone = data.details.phone.mobile
            contact.Fax = data.details.fax
            contact.EMail = data.details.email
            contact.WWW = data.details.website

            contact.Latitude = float(data.geopoint.latitude) \
                               if data.geopoint.latitude else None
            contact.Longitude = float(data.geopoint.longitude) \
                                if data.geopoint.longitude else None

            contact.BirthDate = datetime.strptime(data.birthdate, '%d.%m.%Y') \
                                if data.birthdate else None
            contact.CategoryID = int(data.category)
            contact.Comment = data.comment

            name = str(contact)

            logger.info(f'Updating contact {id} "{name}"')

            db.commit()

            return {'id': id, 'name': name}

    except HTTPException as e:
        raise e

    except Exception as e:

        logger.exception(e)
        db.rollback()

        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to update contact {id}: {e}')


@router.post('/delete/{id}', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                             response_model=Acknowledgment)
def delete(id: int, logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    try:

        with bandbase.core.database.session() as db:

            contact = db.query(Contact).get(id)

            if not contact:

                raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND,
                                    detail=f'Unable to delete contact {id}, it doesn\'t exist!')

            name = str(contact)

            if contact.IsPersistent:
                raise HTTPException(status_code=STATUS.HTTP_400_BAD_REQUEST,
                                    detail=f'Unable to delete contact {id} "{name}", it\'s marked as persistent!')

            if contact.IsReferenced:
                raise HTTPException(status_code=STATUS.HTTP_400_BAD_REQUEST,
                                    detail=f'Unable to delete contact {id} "{name}", it\'s still referenced!')

            logger.info(f'Deleting contact {id} "{name}"')

            db.delete(contact)
            db.commit()

            return {'id': id, 'name': name}

    except HTTPException as e:
        raise e

    except IntegrityError as e:  # TODO ISSUE #16

        logger.exception(e)
        db.rollback()

        raise HTTPException(status_code=STATUS.HTTP_400_BAD_REQUEST,
                            detail=f'Unable to delete contact {id}, it\'s still referenced!')

    except Exception as e:

        logger.exception(e)
        db.rollback()

        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to delete contact {id}: {e}')
