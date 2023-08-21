
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import requests
import json

class HotelReservationCheckin(models.Model):
    _name = "hotel.reservation.checkin"
    _description = "Hotel Reservation Checkin"
    _rec_name = "room_id"

    guest_name = fields.Char("Guest Name", required=True)
    guest_pin = fields.Char("Guest Pin", required=True)
    guest_gender = fields.Char("Gender", required=True)
    guest_designation = fields.Char("Designation", required=True)
    guest_org = fields.Char("Organization", required=True)
    guest_mobile = fields.Char("Mobile", required=True)
    guest_area = fields.Char("Working Area")
    room_id = fields.Many2one("hotel.room","Room")
    #product_id = fields.Many2one("product.product","Room")
    checkin_date = fields.Datetime("Check In", required=True)
    checkout_date = fields.Datetime("Check Out", required=True)
    hotel_reservation_line_id = fields.Many2one("hotel.reservation.line", "Reservation line")
    is_instructor = fields.Boolean("Is Instructor", default=False)



    @api.onchange("guest_pin")
    def _onchange_guest_pin(self):
        if not self.guest_pin:
            return
        text1 = "http://api.brac.net/v1/staffs/"
        text2 = "?Key=AB8F3C5E-CA4D-4604-B3AA-4897DDAE29CF&fields=StaffPIN,StaffName,MobileNo,extension,EmailID,CoreProgramName,ProjectName,DesignationName,BranchName,sex"
        url = text1 + "" + self.guest_pin + "" + text2
        #print(url);
        response = requests.get(url)
        if response.text:
            data = json.loads(response.text)
            print(data[0])
            self.guest_name = data[0]['StaffName']
            self.guest_designation = data[0]['DesignationName']
            self.guest_gender = data[0]['sex']
            self.guest_mobile = data[0]['MobileNo']
            self.guest_org = data[0]['BranchName']
        else:
            self.guest_name = ""
            self.guest_designation = ""
            self.guest_gender = ""
            self.guest_mobile = ""
            self.guest_org = ""
            self.guest_pin = ""
            raise ValidationError(
                _(
                    """Please Enter Valid Pin !"""
                )
            )

class HotelReservationLine(models.Model):
    _inherit = "hotel.reservation.line"
    _description = "Reservation Line"

    checkin_lines = fields.One2many("hotel.reservation.checkin","hotel_reservation_line_id"
                                    ,string="CheckIn Details",)