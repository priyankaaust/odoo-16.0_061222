
from odoo import _, api, fields, models

class TrainerType(models.Model):
    _name = "trainer.type"
    _description = "Trainer Type"

    name = fields.Char(string="Type Name", required=True, copy=False)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the type without removing it.")

class TrainerName(models.Model):
    _name = "trainer.name"
    _rec_name = "name"
    _description = "Trainer Name"
    _order = "name desc"

    name = fields.Char(string="Trainer Name", required=True, copy=False)
    pin = fields.Char(string="Pin",copy=False)
    note = fields.Html(
        string="Terms and conditions",store=True, readonly=False)
    company_id = fields.Many2one(
        "res.company",
        "BLC",
        index=True,default=1)
    partner_id = fields.Many2one(
        "res.partner",
        "partner_id", #required=True,delegate=True,
        #ondelete="cascade",
    )
    trainer_type_id = fields.Many2one("trainer.type","Training Type",)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the trainer without removing it.")

    #@api.model
    #def create(self, vals):
    #    return super(TrainerName, self).create(vals)

class TrainingName(models.Model):
    _name = "training.info"
    _rec_name = "name"
    _description = "Training Details"
    _order = "name desc"

    name = fields.Char("Training Name", required=True, copy=False)
    trainer_type_id = fields.Many2one("trainer.type","Training Type")
    company_id = fields.Many2one(
        "res.company",
        "BLC",
        index=True,
        default=1)
    trainer_lines = fields.One2many(
        "training.info.line",
        "training_id",
        string="Trainer List",
    )
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the training without removing it.")

class TrainingNameLine(models.Model):
    _name = "training.info.line"
    _description = "Training Details Line"

    trainer_id = fields.Many2one("trainer.name")
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    training_id = fields.Many2one("training.info")



