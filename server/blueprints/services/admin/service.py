from server.blueprints.services.admin.model import AdminModel

class AdminService:

    @staticmethod
    def get_dashboard_stats():
        data = {}
        data["total_doctors"] = AdminModel.count_doctors()
        data["specializations"] = AdminModel.count_doctors_by_specialization()
        return data

    @staticmethod
    def get_feedback_ratings():
        return AdminModel.get_feedback_ratings()

    @staticmethod
    def get_all_feedback():
        return AdminModel.get_feedback_list()
