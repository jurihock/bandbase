from parsers.common import *
from utils.models import *

class ContactFormRequestParser(RequestParser):

    def parse(self, contact):

        contact.FirstName    = self.str('first_name')
        contact.LastName     = self.str('last_name')
        contact.FullLastName = self.str('full_last_name')
        contact.BirthDate    = self.date('birth_date')

        newCategoryName = self.str('new_category_name')

        if newCategoryName:

            newCategory = ContactCategory(
                Name=newCategoryName)

            self.db.add(newCategory)
            self.db.flush()
            self.db.refresh(newCategory)

            contact.CategoryID = newCategory.ID

        else:

            contact.CategoryID = self.int('category')

        contact.Street      = self.str('street')
        contact.HouseNumber = self.str('house_number')
        contact.PostalCode  = self.str('postal_code')
        contact.City        = self.str('city')
        contact.Country     = self.str('country')

        contact.LandlinePhone = self.str('landline_phone')
        contact.MobilePhone   = self.str('mobile_phone')
        contact.Fax           = self.str('fax')
        contact.EMail         = self.str('email')
        contact.WWW           = self.str('www')

        contact.Latitude  = self.float('latitude')
        contact.Longitude = self.float('longitude')

        contact.Comment = self.str('comment')
