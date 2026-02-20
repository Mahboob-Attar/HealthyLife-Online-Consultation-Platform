from server.blueprints.services.appointments.model import AppointmentModel

class AppointmentService:

    @staticmethod
    def load_appointment_page(search_query=None):
        """
        Load doctors for appointment page
        Supports search by specialization or services (symptoms)
        """

        # 🔎 Search doctors if query provided
        if search_query:
            doctors = AppointmentModel.search_doctors(search_query)
        else:
            doctors = AppointmentModel.get_all_doctors()

        # 🖼 Assign default images if missing
        for doc in doctors:
            doc["photo_path"] = doc.get("photo_path") or "default.jpg"

        return {
            "doctors": doctors
        }