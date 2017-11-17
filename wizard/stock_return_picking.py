# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    return_time_expired = fields.Boolean(
        compute='_compute_return_time_expired',
        string='Time expired for return')

    @api.depends('location_id', 'return_reason_id')
    def _compute_return_time_expired(self):
        """Computes value of field return_time_expired"""

        StockPicking = self.env['stock.picking']
        picking_id = self._context and self._context.get('active_id', False) \
            or False
        picking = StockPicking.browse(picking_id)
        return_time_expiration_days = \
            self.env.user.company_id.sale_return_time_expiration_days

        if return_time_expiration_days > 0:

            picking_date_done = datetime.strptime(
                picking.date_done, '%Y-%m-%d %H:%M:%S')

            picking_days_done = (datetime.now() - picking_date_done).days

            if picking_days_done >= return_time_expiration_days:
                self.return_time_expired = True
                parent_location = picking.location_id.location_id
                StockLocation = self.env['stock.location']
                location_return_not_accepted = StockLocation.search([
                    ('return_not_accepted_location', '=', True),
                    ('location_id', '=', parent_location.id),
                    ])

                if location_return_not_accepted:
                    self.location_id = location_return_not_accepted[0]

                    return_reason_time_expired = self.env.ref(
                        'sale_stock_restrict_return_picking_expiration_time.return_time_expired')

                    if return_reason_time_expired:
                        self.return_reason_id = return_reason_time_expired

                    else:
                        raise ValidationError(
                            _('The return reason "Time Expired for Return" has been deleted. Go with system admin for update module "Restrict return pickings from pickings of sales orders expired"')
                        )

                else:
                    raise ValidationError(
                        _('This return cannot be made, the time to make the return has expired, you must set up a location of non-accepted returns.')
                    )

    @api.v7
    def default_get(self, cr, uid, fields, context=None):

        res = super(StockReturnPicking, self).default_get(
            cr, uid, fields, context=context)

        if 'location_id' in fields:
            StockPicking = self.pool.get('stock.picking')
            picking_id = context and context.get('active_id', False) \
                or False
            picking = StockPicking.browse(cr, uid, picking_id, context=context)
            ResUsers = self.pool.get('res.users')
            user = ResUsers.browse(cr, uid, uid, context=context)
            return_time_expiration_days = \
                user.company_id.sale_return_time_expiration_days

            if return_time_expiration_days > 0:

                picking_date_done = datetime.strptime(
                    picking.date_done, '%Y-%m-%d %H:%M:%S')

                picking_days_done = (datetime.now() - picking_date_done).days

                if picking_days_done >= return_time_expiration_days:
                    parent_location = picking.location_id.location_id
                    StockLocation = self.pool.get('stock.location')
                    location_return_not_accepted = StockLocation.search(
                        cr, uid, [
                            ('return_not_accepted_location', '=', True),
                            ('location_id', '=', parent_location.id),
                            ], context=context)

                    if location_return_not_accepted:
                        if res.get('location_id', False):
                            res['location_id'] = location_return_not_accepted[0]

                        IrModelData = self.pool.get('ir.model.data')

                        return_reason_time_expired = \
                            IrModelData.get_object_reference(
                                cr,
                                uid,
                                'sale_stock_restrict_return_picking_expiration_time',
                                'return_time_expired')[1]

                        if return_reason_time_expired:                            
                            res['return_reason_id'] = return_reason_time_expired

                        else:
                            raise ValidationError(
                                _('The return reason "Time Expired for Return" has been deleted. Go with system admin for update module "Restrict return pickings from pickings of sales orders expired"')
                            )

                    else:
                        raise ValidationError(
                            _('This return cannot be made, the time to make the return has expired, you must set up a location of non-accepted returns.')
                        )
        return res
