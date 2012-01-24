#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


from xml.etree import ElementTree as ET



def write_jmeter_output(mm_data, output_path):
    """
    Take the list of ResponseStats objects and write a JMeter 2.1
    formatted XML file to output_path.

    JMeter JTL file documentation:
    http://jakarta.apache.org/jmeter/usermanual/listeners.html
    """
    root = ET.Element('testResults')
    root.set('version', "1.2")

    for test_transaction in mm_data:
        # each transaction might have multiple timers
        transaction_root = ET.SubElement(root, 'sample')
        # JMeter uses ms for time
        ms_trans_time = test_transaction.trans_time * 1000
        transaction_root.set('t', '%d' % ms_trans_time)
        ms_timestamp = test_transaction.epoch_secs * 1000
        transaction_root.set('ts', '%d' % ms_timestamp)
        transaction_root.set('lb', test_transaction.user_group_name)  # label
        transaction_root.set('sc', '1')  # sample count

        if test_transaction.error:
            transaction_root.set('ec', '1') # was an error
            transaction_root.set('s', 'false') # was an error
            # errors don't have custom_timers
            continue
        else:
            transaction_root.set('ec', '0')
            transaction_root.set('s', 'true')

        # parse the custom_timers and add each as a JMeter sub-sample
        for timer_name, timer_duration in test_transaction.custom_timers.items():
            timer_duration = float(timer_duration)
            timer_element = ET.SubElement(transaction_root, 'sample')
            ms_trans_time = timer_duration * 1000
            timer_element.set('t', '%d' % ms_trans_time)
            # subtimers don't have timestamps, so use the Transaction ts
            timer_element.set('ts', '%d' % ms_timestamp)
            timer_element.set('lb', timer_name)
            timer_element.set('sc', '1')
            timer_element.set('ec', '0')
            timer_element.set('s', 'true')

    tree = ET.ElementTree(root)
    tree.write(output_path + '/results.jtl')
    tree.write('last_results.jtl')
