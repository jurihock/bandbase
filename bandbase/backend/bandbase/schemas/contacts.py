from pydantic import BaseModel
from typing import Dict, List, Optional, Union


class ContactName(BaseModel):
    first: Optional[str]
    last: str
    full: Optional[str]


class ContactAddress(BaseModel):
    street: Optional[str]
    house: Optional[str]
    city: Optional[str]
    zip: Optional[str]
    country: Optional[str]


class ContactPhone(BaseModel):
    landline: Optional[str]
    mobile: Optional[str]


class ContactDetails(BaseModel):
    phone: ContactPhone
    fax: Optional[str]
    email: Optional[str]
    website: Optional[str]


class ContactGeopoint(BaseModel):
    latitude: Optional[Union[float, str]]
    longitude: Optional[Union[float, str]]


class ContactData(BaseModel):
    name: ContactName
    address: ContactAddress
    details: ContactDetails
    geopoint: ContactGeopoint
    birthdate: Optional[str]
    category: Union[int, str]
    comment: Optional[str]
