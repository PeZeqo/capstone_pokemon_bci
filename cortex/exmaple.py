from cortex import Cortex
import json
from record import Record


def do_stuff(cortex):
    # await cortex.inspectApi()
    print("** GET CORTEX INFO **")
    cortex.get_cortex_info()
    print("** GET USER LOGIN **")
    cortex.get_user_login()
    print("** REQUEST ACCESS **")
    cortex.request_access()
    print("** AUTHORIZE **")
    cortex.authorize()
    print("** QUERY HEADSETS **")
    cortex.query_headset()

    if len(cortex.headsets) > 0:
        print("** CREATE SESSION **")
        cortex.create_session(activate=True, headset_id=cortex.headsets[0])
        print("** CREATE RECORD **")
        cortex.create_record(title="test record 1")
        print("** SUBSCRIBE POW & MET **")
        cortex.subscribe(['eeg'])
        while cortex.packet_count < 10:
            cortex.get_data()
        cortex.inject_marker(label='halfway', value=1,
                                   time=cortex.to_epoch())
        while cortex.packet_count < 20:
            cortex.get_data()
        cortex.close_session()


def main():
    with open('cred.json') as json_file:
        user = json.load(json_file)
    cortex = Cortex(user, True)
    # do_stuff(cortex)
    record = Record(cortex)
    record.run()


if __name__ == '__main__':
    main()
