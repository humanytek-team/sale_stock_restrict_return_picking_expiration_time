# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': "Restrict return pickings from pickings of sales orders expired",
    'description': """
    Restrict return pickings from pickings of sales orders whose time has
    expired.
    """,
    'author': "Humanytek",
    'website': "http://www.humanytek.com",
    'category': 'Stock',
    'version': '0.1.0',
    'depends': [
        'sale',
        'stock',
        'stock_warehouse_returns',
        'stock_return_picking_with_reason', ],
    'data': [
        'data/stock_warehouse_returns_data.xml',
        'views/res_company_view.xml',
        'wizard/stock_return_picking_view.xml',
    ],
    'demo': [
    ],
}
