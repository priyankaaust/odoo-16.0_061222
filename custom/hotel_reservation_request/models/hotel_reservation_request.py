
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

RESERVATION_TYPE = [
    ('Official', 'Official'),
    ('Personal', 'Personal')
]

RESERVATION_PURPOSE = [
    ('Training', 'Training'),
    ('Accommodation', 'Accommodation')
]

TRAINING_CONDUCTED_BY = [
    ('LLD Facilitator', 'LLD Facilitator'),
    ('Programme Facilitator', 'Programme Facilitator')
]

class HotelReservationRequest(models.Model):
    _name = "hotel.request"
    _rec_name = "request_no"
    _description = "Reservation Request"
    _order = "request_no desc"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    request_no = fields.Char("Request No", readonly=True, copy=False)
    date_order = fields.Datetime(
        "Date Ordered",
        readonly=True,
        required=True,
        index=True,
        default=lambda self: fields.Datetime.now(),
    )
    company_id = fields.Many2one(
        "res.company",
        "BLC",
        readonly=True,
        index=True,
        required=True,
        default=1,
        states={"draft": [("readonly", False)]},
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Guest Name",
        readonly=True,
        index=True,
        states={"draft": [("readonly", False)]},
    )
    partner_name = fields.Char("Guest Name", readonly=True,
            copy=False,states={"draft": [("readonly", False)]},
    )
    partner_pin = fields.Char("Guest Pin", readonly=True,
            copy=False, states={"draft": [("readonly", False)]},
    )

    reservation_id = fields.Many2one(
        "hotel.reservation",
        "Reservation",
    )
    checkin = fields.Datetime(
        "Date From",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    checkout = fields.Datetime(
        "Date To",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    adults = fields.Integer(
        "Adults",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="List of adults there in guest list. ",
    )
    children = fields.Integer(
        "Children",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Number of children there in guest list.",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirm"),
            ("cancel", "Cancel"),
            ("done", "Done"),
        ],
        "State",
        readonly=True,
        default="draft",
    )
    request_line = fields.One2many(
        "hotel.request.line",
        "line_id",
        string="Request Line",
        help="Hotel room Request details.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    note = fields.Html(
        string="Terms and conditions",
        store=True, readonly=False,)
    reservation_type = fields.Selection(
        selection=RESERVATION_TYPE,
        string="Reservation Type",
        readonly=True,
        copy=False, states={"draft": [("readonly", False)]},store=True)
    reservation_purpose = fields.Selection(
        selection=RESERVATION_PURPOSE,
        string="Reservation Purpose",
        readonly=True,
        copy=False, states={"draft": [("readonly", False)]}, store=True)
    training_conducted = fields.Selection(
        selection=TRAINING_CONDUCTED_BY,
        string="Training Conducted By",
        readonly=True,
        copy=False, states={"draft": [("readonly", False)]}, store=True)

    facilitator_pin = fields.Char("Facilitator Pin", readonly=True,
        copy=False, states={"draft": [("readonly", False)]},
        )
    training_id = fields.Many2one(
        "training.info",
        "Training",
        states={"draft": [("readonly", False)]},
    )
    training_checkin = fields.Datetime(
        "Training Start Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    training_checkout = fields.Datetime(
        "Training End Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )




    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        vals["request_no"] = (
                self.env["ir.sequence"].next_by_code("hotel.request") or "New"
        )
        return super(HotelReservationRequest, self).create(vals)

    def create_reservation(self):
        for request in self:
            print(request.partner_name)
            customerName = None
            if not request.partner_pin:
                customerName = request.partner_name
            else:
                customerName = request.partner_pin + "_" + request.partner_name
            customer = self.env['res.partner'].search([('name','ilike',customerName)])
            if not customer:
                customerValues = {
                    'name' : customerName
                }
                customer = self.env['res.partner'].create(customerValues)

            values = {
                'company_id': request.company_id.id,
                'training_id': request.training_id.id,
                'partner_id': customer.id,
                'pricelist_id': 1,
                'partner_order_id': customer.id,
                'partner_invoice_id': customer.id,
                'partner_shipping_id': customer.id,
                'checkin': request.checkin,
                'checkout' : request.checkout,
                'adults' : request.adults,
                'children' : request.children,
                'reservation_no': "",
                #'reservation_line': []
            }
            reservation = self.env['hotel.reservation'].create(values)
            print(reservation)
            if reservation.id:
                for line in request.request_line:
                    line_values = {
                        'categ_id': line.categ_id.id,
                        'line_id' : reservation.id,
                    }
                    self.env['hotel.reservation.line'].create(line_values)
            request.write({'reservation_id':reservation.id,'state':'confirm'})

            return {
                'name': _('Reservation'),
                'view_mode': 'form',
                'res_model': 'hotel.reservation',
                'res_id': reservation.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }



class HotelRequestLine(models.Model):

    _name = "hotel.request.line"
    _description = "Request Line"

    name = fields.Char("Name")
    line_id = fields.Many2one("hotel.request")
    request = fields.Many2many(
        "hotel.room",
        "hotel_request_line_room_rel",
        "hotel_request_line_id",
        "room_id",
        domain="[('isroom','=',True),('categ_id','=',categ_id)]",
    )
    categ_id = fields.Many2one("hotel.room.type", "Room Type")

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

    @api.onchange("categ_id")
    def on_change_categ(self):
        """
        When you change categ_id it check checkin and checkout are
        filled or not if not then raise warning
        -----------------------------------------------------------
        @param self: object pointer
        """
        if not self.line_id.checkin:
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
        room_ids = []
        for room in hotel_room_ids:
            assigned = False
            for line in room.room_reservation_line_ids.filtered(
                    lambda l: l.status != "cancel"
            ):
                if self.line_id.checkin and line.check_in and self.line_id.checkout:
                    if (
                            self.line_id.checkin <= line.check_in <= self.line_id.checkout
                    ) or (
                            self.line_id.checkin <= line.check_out <= self.line_id.checkout
                    ):
                        assigned = True
                    elif (line.check_in <= self.line_id.checkin <= line.check_out) or (
                            line.check_in <= self.line_id.checkout <= line.check_out
                    ):
                        assigned = True
            for rm_line in room.room_line_ids.filtered(lambda l: l.status != "cancel"):
                if self.line_id.checkin and rm_line.check_in and self.line_id.checkout:
                    if (
                            self.line_id.checkin
                            <= rm_line.check_in
                            <= self.line_id.checkout
                    ) or (
                            self.line_id.checkin
                            <= rm_line.check_out
                            <= self.line_id.checkout
                    ):
                        assigned = True
                    elif (
                            rm_line.check_in <= self.line_id.checkin <= rm_line.check_out
                    ) or (
                            rm_line.check_in <= self.line_id.checkout <= rm_line.check_out
                    ):
                        assigned = True
            if not assigned:
                room_ids.append(room.id)
        domain = {"request": [("id", "in", room_ids)]}
        return {"domain": domain}

class HotelReservation(models.Model):
    _inherit = "hotel.reservation"

    training_id = fields.Many2one(
        "training.info",
        "Training",
        states={"draft": [("readonly", False)]},
    )


