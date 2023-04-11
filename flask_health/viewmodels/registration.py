class RegistrationViewModel:
    def __init__(
        self,
        id,
        order_no,
        order_date,
        payment_method,
        patient_name,
        doctor_name,
        status,
    ):
        self.id = id
        self.order_no = order_no
        self.order_date = order_date
        self.payment_method = payment_method
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.status = status
