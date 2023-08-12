import schedule
import time


class Scheduler:
    def __init__(self, image_shield):
        self.scheduler = schedule
        self.image_shield = image_shield

    def run(self):
        self.scheduler.every(2).seconds.do(self.execute_job)
        while True:
            self.scheduler.run_all()
            time.sleep(1)

    def execute_job(self):
        # TODO to check if there is still an ongoing meeting

        if self.image_shield.window:
            print("Remove Shield")
            self.image_shield.remove_shield()
        else:
            print("Put Shield")
            self.image_shield.put_shield()
