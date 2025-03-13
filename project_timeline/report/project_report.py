# Copyright 2024 Tecnativa - Carlos López
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    planned_date_start = fields.Datetime(readonly=True)
    planned_date_end = fields.Datetime(readonly=True)

    def _select(self):
        res = super()._select()
        if "planned_date_end" in res:
            return (
                res
                + """,
            t.planned_date_start"""
            )
        return (
            res
            + """,
            t.planned_date_start as planned_date_start,
            t.planned_date_end as planned_date_end
        """
        )

    def _group_by(self):
        res = super()._group_by()
        if "planned_date_end" in res:
            return (
                res
                + """,
            t.planned_date_start"""
            )
        return (
            res
            + """,
            planned_date_start,
            planned_date_end
        """
        )
