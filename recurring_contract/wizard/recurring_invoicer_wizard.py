﻿# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Cyril Sester <csester@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################

from odoo import fields, models, api
from odoo.tools.translate import _


class recurring_invoicer_wizard(models.TransientModel):

    ''' This wizard generate invoices from contract groups when launched.
    By default, all contract groups are used.
    '''
    _name = 'recurring.invoicer.wizard'

    generation_date = fields.Date(_('Generation date'), readonly=True)

    @api.multi
    def generate(self):
        recurring_invoicer_obj = self.env['recurring.invoicer']
        contract_groups = self.env['recurring.contract.group'].search([])
        invoicer = recurring_invoicer_obj.create({'source': self._name})

        contract_groups.with_context(async_mode=False).generate_invoices(
            invoicer)

        return {
            'name': 'recurring.invoicer.form',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': invoicer.id,  # id of the object to which to redirect
            'res_model': 'recurring.invoicer',  # object name
            'type': 'ir.actions.act_window',
        }

    @api.model
    def generate_from_cron(self):
        res = self.with_context(async_mode=False).generate()
        invoicer_id = res['res_id']
        invoicer = self.env['recurring.invoicer'].browse(invoicer_id)
        invoicer.validate_invoices()
