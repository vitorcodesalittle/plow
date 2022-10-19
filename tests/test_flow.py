from decorators import plow



def test_plow():
    @plow
    def send_email(email: str, email_template: str):
        pass

    @plow
    def ifelse(if_: str, then: str, else_: str):
        pass


    @plow
    def wait(if_: str, then_: str, else_: str):
        pass

    @plow
    def send_email(email: str, email_template: str):
        pass

    @plow
    def check_response(email: str):
        pass
