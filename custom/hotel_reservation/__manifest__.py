# See LICENSE file for full copyright and licensing details.

{
    "name": "Hotel Reservation Management",
    "version": "14.0.1.0.0",
    "author": "Odoo Community Association (OCA), Serpent Consulting \
                Services Pvt. Ltd., Odoo S.A.",
    "category": "Generic Modules/Hotel Reservation",
    "license": "AGPL-3",
    "summary": "Manages Guest Reservation & displays Reservation Summary",
    "website": "https://github.com/OCA/vertical-hotel",
    "depends": ["hotel", "stock", "mail"],
    "demo": ["data/hotel_reservation_data.xml"],
    "data": [
        "security/ir.model.access.csv",
        "data/hotel_scheduler.xml",
        "data/hotel_reservation_sequence.xml",
        "data/email_template_view.xml",
        "views/hotel_reservation_view.xml",
        "report/checkin_report_template.xml",
        "report/checkout_report_template.xml",
        "report/room_max_report_template.xml",
        "report/hotel_reservation_report_template.xml",
        "report/report_view.xml",
        #"views/assets.xml",
        "wizards/hotel_reservation_wizard.xml",
    ],
    "assets": {
        'hotel_reservation.assets': [
               'hotel_reservation/static/src/css/room_kanban.css',
	],
        "web.assets_backend": [
		'hotel_reservation/static/src/js/hotel_room_summary.js',],
    },
    "qweb": ["static/src/xml/hotel_room_summary.xml"],
    "external_dependencies": {"python": ["dateutil"]},
    "installable": True,
}
