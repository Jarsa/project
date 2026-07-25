# Copyright 2023 - Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo.addons.base.tests.common import BaseCommon


class TestProjectTaskPurchase(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": cls.project.id,
            }
        )
        cls.vendor = cls.env["res.partner"].create({"name": "Test Vendor"})

    def _create_purchase_order(self):
        return self.env["purchase.order"].create(
            {
                "partner_id": self.vendor.id,
                "task_id": self.task.id,
                "origin": self.task.name,
            }
        )

    def test_action_create_purchase_order(self):
        action = self.task.action_create_purchase_order()
        self.assertEqual(action["res_model"], "purchase.order")
        self.assertEqual(action["context"]["default_task_id"], self.task.id)
        self.assertEqual(action["context"]["default_origin"], self.task.name)

    def test_purchase_order_count(self):
        self.assertEqual(self.task.purchase_order_count, 0)
        order = self._create_purchase_order()
        self.assertEqual(self.task.purchase_order_count, 1)
        self.assertEqual(self.task.purchase_order_ids, order)

    def test_action_view_purchase_orders_single(self):
        order = self._create_purchase_order()
        action = self.task.action_view_purchase_orders()
        self.assertEqual(action["res_id"], order.id)
        self.assertEqual(action["view_mode"], "form")

    def test_action_view_purchase_orders_multiple(self):
        orders = self._create_purchase_order() | self._create_purchase_order()
        action = self.task.action_view_purchase_orders()
        self.assertEqual(action["view_mode"], "list,form")
        domain_field, domain_operator, domain_ids = action["domain"][0]
        self.assertEqual((domain_field, domain_operator), ("id", "in"))
        self.assertCountEqual(domain_ids, orders.ids)

    def test_action_view_task(self):
        order = self._create_purchase_order()
        action = order.action_view_task()
        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(action["res_id"], self.task.id)
