{
    "name": "Hotel Reservation Request",
    "version": "16.0.0.0.0",
    "author": "Priyanka",
    "category": "Generic Modules/Hotel Reservation_request",
    "license": "AGPL-3",
    "summary": "Manages Guest Reservation Request",
    "depends": ["hotel", "mail"],
    "external_dependencies": {"python": ["dateutil"]},
    "data": [
        "security/ir.model.access.csv",
        "data/hotel_request.xml",
        "views/hotel_Reservation_request.xml",
        "views/hotel_checkin_view.xml",
    ],
    "installable": True,

}