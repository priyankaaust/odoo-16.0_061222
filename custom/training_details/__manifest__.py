{
    "name": "Training Details",
    "version": "16.0.0.0.0",
    "author": "Priyanka",
    "category": "Generic Modules/Training_Details",
    "license": "AGPL-3",
    "summary": "Manages Training Details",
    "depends": ["base","mail"],
    "external_dependencies": {"python": ["dateutil"]},
    "data": [
        "security/ir.model.access.csv",
        "views/training_details_view.xml",
    ],
    "installable": True,

}