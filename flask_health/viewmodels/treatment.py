class TreatmentViewModel:
    def __init__(
        self,
        id,
        order_no,
        order_date,
        patient_name,
        doctor_name,
        order_status,
    ):
        self.id = id
        self.order_no = order_no
        self.order_date = order_date
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.order_status = order_status
