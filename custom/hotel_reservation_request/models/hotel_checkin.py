
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class HotelCheckIn(models.Model):
    _name = "hotel.checkin"
    _description = "Hotel Checkin"

    checkin_no = fields.Char("CheckIn No", readonly=True, copy=False)
    reservation_id = fields.Many2one(
        "hotel.reservation",
        "Reservation",
    )
    checkin = fields.Datetime(
        "Expected-Date-Arrival",
    )
    checkout = fields.Datetime(
        "Expected-Date-Departure",
    )
    adults = fields.Integer(
        "Adults",
        help="List of adults there in guest list. ",
    )
    children = fields.Integer(
        "Children",
        help="Number of children there in guest list.",
    )
    checkin_lines = fields.One2many(
        "hotel.checkin.line",
        "hotel_checkin_id",
        string="CheckIn Line",
        help="Hotel room Checkin details.",
    )
    training_id = fields.Many2one(
        "training.info",
        "Training",
    )
    company_id = fields.Many2one(
        "res.company",
        "BLC",
        index=True,
        required=True,
        default=1,
    )

    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        vals["request_no"] = (
                self.env["ir.sequence"].next_by_code("hotel.checkin") or "New"
        )
        return super(HotelCheckIn, self).create(vals)

    @api.onchange("reservation_id")
    def _onchange_reservation_id(self):
        if self.reservation_id:
            self.update(
                {
                    "company_id": self.reservation_id.company_id.id,
                    "training_id": self.reservation_id.training_id.id,
                    "checkin": self.reservation_id.checkin,
                    "checkout": self.reservation_id.checkout,
                    "adults":self.reservation_id.adults,
                    "children":self.reservation_id.children,
                }
            )



class HotelCheckInLine(models.Model):
    _name = "hotel.checkin.line"
    _description = "Hotel Checkin Line"

    hotel_checkin_id = fields.Many2one("hotel.checkin")
    categ_id = fields.Many2one("hotel.room.type", "Room Type")
    room_id = fields.Many2one(
        "hotel.room",
        "Room",
    )
    partner_name = fields.Char("Guest Name",copy=False,)
    partner_pin = fields.Char("Guest Pin",copy=False,)
    checkin = fields.Datetime(
        "DateTime-Arrival",
        required=True,
    )
    checkout = fields.Datetime(
        "DateTime-Departure",
        required=True,
    )
    guest_checkin_line = fields.Many2many(
        "hotel.guest.checkin.line",
        "guest_checkin_line_rel",
        "hotel_checkin_line_id",
        "hotel_guest_checkin_line_id",
        #domain="[('isroom','=',True),('categ_id','=',categ_id)]",
    )

    @api.onchange("categ_id")
    def on_change_categ(self):
        """
        When you change categ_id it check checkin and checkout are
        filled or not if not then raise warning
        -----------------------------------------------------------
        @param self: object pointer
        """
        if not self.hotel_checkin_id.checkin:
            raise ValidationError(
                _(
                    """Before choosing a room,\n You have to """
                    """select a Check in date or a Check out """
                    """ date in the reservation form."""
                )
            )
        hotel_room_ids = self.env["hotel.room"].search(
            [("room_categ_id", "=", self.categ_id.id)]
        )
        print(hotel_room_ids)
        room_ids = []
        for room in hotel_room_ids:
            assigned = False
            for line in room.room_reservation_line_ids.filtered(
                    lambda l: l.status != "cancel"
            ):
                if self.hotel_checkin_id.checkin and line.check_in and self.hotel_checkin_id.checkout:
                    if (
                            self.hotel_checkin_id.checkin <= line.check_in <= self.hotel_checkin_id.checkout
                    ) or (
                            self.hotel_checkin_id.checkin <= line.check_out <= self.hotel_checkin_id.checkout
                    ):
                        assigned = True
                    elif (line.check_in <= self.hotel_checkin_id.checkin <= line.check_out) or (
                            line.check_in <= self.hotel_checkin_id.checkout <= line.check_out
                    ):
                        assigned = True
            for rm_line in room.room_line_ids.filtered(lambda l: l.status != "cancel"):
                if self.hotel_checkin_id.checkin and rm_line.check_in and self.hotel_checkin_id.checkout:
                    if (
                            self.hotel_checkin_id.checkin
                            <= rm_line.check_in
                            <= self.hotel_checkin_id.checkout
                    ) or (
                            self.hotel_checkin_id.checkin
                            <= rm_line.check_out
                            <= self.hotel_checkin_id.checkout
                    ):
                        assigned = True
                    elif (
                            rm_line.check_in <= self.hotel_checkin_id.checkin <= rm_line.check_out
                    ) or (
                            rm_line.check_in <= self.hotel_checkin_id.checkout <= rm_line.check_out
                    ):
                        assigned = True
            if not assigned:
                room_ids.append(room.id)
        domain = {"room_id": [("id", "in", room_ids)]}
        print(domain)
        return {"domain": domain}

class HotelGuestCheckInLine(models.Model):
    _name = "hotel.guest.checkin.line"
    _description = "Hotel Guest Checkin Line"

    guest_name = fields.Char("Guest Name", required=True)
    guest_pin = fields.Char("Guest Pin", required=True)
    guest_gender = fields.Char("Gender", required=True)
    guest_designation = fields.Char("Designation", required=True)
    guest_org = fields.Char("Organization", required=True)
    guest_mobile = fields.Char("Mobile", required=True)
    guest_area = fields.Char("Working Area", required=True)
    room_id = fields.Many2one("hotel.room","Room")
    hotel_checkin_line_id = fields.Many2one("hotel.checkin.line")