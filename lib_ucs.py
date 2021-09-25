#!/usr/bin/env python3

import codecs
import copy
import ipaddress
import jinja2
import os, re, sys
import pkg_resources
import validating_ucs
from pathlib import Path

ucs_template_path = pkg_resources.resource_filename('lib_ucs', 'ucs_templates/')

class config_conversion(object):
    def __init__(self, json_data, type):
        self.json_data = json_data
        self.templateLoader = jinja2.FileSystemLoader(
            searchpath=(ucs_template_path + '%s/') % (type))
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)
        self.templateVars = {}
        self.type = type
        self.orgs = []
        for item in json_data['config']['orgs']:
            for k, v in item.items():
                if k == 'name':
                    self.orgs.append(v)

    def bios_policies(self):
        header = 'BIOS Policy Variables'
        initial_policy = True
        template_type = 'bios_policies'

        # Set the org_count to 0 for the First Organization
        org_count = 0

        # Loop through the orgs discovered by the Class
        for org in self.orgs:

            # Pull in Variables from Class
            templateVars = self.templateVars
            templateVars['org'] = org

            # Define the Template Source
            templateVars['header'] = header
            templateVars['template_type'] = template_type
            template_file = "template_open.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            if initial_policy == True:
                write_method = 'w'
            else:
                write_method = 'a'
            process_method(write_method, dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = '%s.jinja2' % (template_type)
            template = self.templateEnv.get_template(template_file)

            if template_type in self.json_data['config']['orgs'][org_count]:
                for item in self.json_data['config']['orgs'][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars['org'] = org

                    # Define the Template Source
                    templateVars['header'] = header

                    for k, v in item.items():
                        if (k == 'name' or k == 'descr' or k == 'tags'):
                            templateVars[k] = v

                    templateVars['bios_settings'] = {}
                    for k, v in item.items():
                        if not (k == 'name' or k == 'descr' or k == 'tags'):
                            templateVars['bios_settings'][k] = v

                    # Process the template
                    dest_dir = '%s' % (self.type)
                    dest_file = '%s.auto.tfvars' % (template_type)
                    process_method('a', dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = "template_close.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            process_method('a', dest_dir, dest_file, template, **templateVars)

            # Increment the org_count for the next Organization Loop
            org_count += 1

    def boot_order_policies(self):
        header = 'Boot Order Policy Variables'
        initial_policy = True
        template_type = 'boot_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ethernet_adapter_policies(self):
        header = 'Ethernet Adapter Policy Variables'
        initial_policy = True
        template_type = 'ethernet_adapter_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ethernet_network_control_policies(self):
        header = 'Ethernet Network Control Policy Variables'
        initial_policy = True
        template_type = 'ethernet_network_control_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ethernet_network_group_policies(self):
        header = 'Ethernet Network Group Policy Variables'
        initial_policy = True
        template_type = 'ethernet_network_group_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ethernet_network_policies(self):
        header = 'Ethernet Network Policy Variables'
        initial_policy = True
        template_type = 'ethernet_network_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ethernet_qos_policies(self):
        header = 'Ethernet QoS Policy Variables'
        initial_policy = True
        template_type = 'ethernet_qos_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def fibre_channel_adapter_policies(self):
        header = 'Fibre Channel Adapter Policy Variables'
        initial_policy = True
        template_type = 'fibre_channel_adapter_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def fibre_channel_network_policies(self):
        header = 'Fibre Channel Network Policy Variables'
        initial_policy = True
        template_type = 'fibre_channel_network_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def fibre_channel_qos_policies(self):
        header = 'Fibre Channel QoS Policy Variables'
        initial_policy = True
        template_type = 'fibre_channel_qos_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def flow_control_policies(self):
        header = 'Flow Control Policy Variables'
        initial_policy = True
        template_type = 'flow_control_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def imc_access_policies(self):
        header = 'IMC Access Policiy Variables'
        initial_policy = True
        template_type = 'imc_access_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ip_pools(self):
        header = 'IP Pool Variables'
        initial_policy = True
        template_type = 'ip_pools'

        # Set the org_count to 0 for the First Organization
        org_count = 0

        # Loop through the orgs discovered by the Class
        for org in self.orgs:

            # Pull in Variables from Class
            templateVars = self.templateVars
            templateVars['org'] = org

            # Define the Template Source
            templateVars['header'] = header
            templateVars['template_type'] = template_type
            template_file = "template_open.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            if initial_policy == True:
                write_method = 'w'
            else:
                write_method = 'a'
            process_method(write_method, dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = '%s.jinja2' % (template_type)
            template = self.templateEnv.get_template(template_file)

            if template_type in self.json_data['config']['orgs'][org_count]:
                for item in self.json_data['config']['orgs'][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars['org'] = org

                    # Define the Template Source
                    templateVars['header'] = header

                    for k, v in item.items():
                        templateVars[k] = v

                    if 'ipv6_blocks' in templateVars:
                        index_count = 0
                        for i in templateVars['ipv6_blocks']:
                             index_count += 1

                        for r in range(0,index_count):
                            if 'to' in templateVars['ipv6_blocks'][r]:
                                templateVars['ipv6_blocks'][r]['size'] = templateVars['ipv6_blocks'][r].pop('to')
                                templateVars['ipv6_blocks'][r]['size'] = int(
                                    ipaddress.IPv6Address(templateVars['ipv6_blocks'][r]["size"])
                                    ) - int(ipaddress.IPv6Address(templateVars['ipv6_blocks'][r]["from"])) + 1

                    # Process the template
                    dest_dir = '%s' % (self.type)
                    dest_file = '%s.auto.tfvars' % (template_type)
                    process_method('a', dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = "template_close.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            process_method('a', dest_dir, dest_file, template, **templateVars)

            # Increment the org_count for the next Organization Loop
            org_count += 1

    def ipmi_over_lan_policies(self):
        header = 'IPMI over LAN Policy Variables'
        initial_policy = True
        template_type = 'ipmi_over_lan_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def iqn_pools(self):
        header = 'IQN Pool Variables'
        initial_policy = True
        template_type = 'iqn_pools'

        # Set the org_count to 0 for the First Organization
        org_count = 0

        # Loop through the orgs discovered by the Class
        for org in self.orgs:

            # Pull in Variables from Class
            templateVars = self.templateVars
            templateVars['org'] = org

            # Define the Template Source
            templateVars['header'] = header
            templateVars['template_type'] = template_type
            template_file = "template_open.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            if initial_policy == True:
                write_method = 'w'
            else:
                write_method = 'a'
            process_method(write_method, dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = '%s.jinja2' % (template_type)
            template = self.templateEnv.get_template(template_file)

            if template_type in self.json_data['config']['orgs'][org_count]:
                for item in self.json_data['config']['orgs'][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars['org'] = org

                    # Define the Template Source
                    templateVars['header'] = header

                    for k, v in item.items():
                        templateVars[k] = v

                    if 'iqn_blocks' in templateVars:
                        index_count = 0
                        for i in templateVars['iqn_blocks']:
                             index_count += 1

                        for r in range(0,index_count):
                            if 'to' in templateVars['iqn_blocks'][r]:
                                templateVars['iqn_blocks'][r]['size'] = templateVars['iqn_blocks'][r].pop('to')
                                templateVars['iqn_blocks'][r]['size'] = int(
                                    templateVars['iqn_blocks'][r]["size"]
                                    ) - int(templateVars['iqn_blocks'][r]["from"]) + 1

                    # Process the template
                    dest_dir = '%s' % (self.type)
                    dest_file = '%s.auto.tfvars' % (template_type)
                    process_method('a', dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = "template_close.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            process_method('a', dest_dir, dest_file, template, **templateVars)

            # Increment the org_count for the next Organization Loop
            org_count += 1

    def iscsi_adapter_policies(self):
        header = 'iSCSI Adapter Policy Variables'
        initial_policy = True
        template_type = 'iscsi_adapter_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def iscsi_boot_policies(self):
        header = 'iSCSI Boot Policy Variables'
        initial_policy = True
        template_type = 'iscsi_boot_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def iscsi_static_target_policies(self):
        header = 'iSCSI Static Target Policy Variables'
        initial_policy = True
        template_type = 'iscsi_static_target_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def lan_connectivity_policies(self):
        header = 'LAN Connectivity Policy Variables'
        initial_policy = True
        template_type = 'lan_connectivity_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def link_aggregation_policies(self):
        header = 'Link Aggregation Policy Variables'
        initial_policy = True
        template_type = 'link_aggregation_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def link_control_policies(self):
        header = 'Link Control Policy Variables'
        initial_policy = True
        template_type = 'link_control_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def mac_pools(self):
        header = 'MAC Pool Variables'
        initial_policy = True
        template_type = 'mac_pools'

        policy_loop_standard(self, header, initial_policy, template_type)

    def multicast_policies(self):
        header = 'Multicast Policy Variables'
        initial_policy = True
        template_type = 'multicast_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def network_connectivity_policies(self):
        header = 'Network Connectivity (DNS) Policy Variables'
        initial_policy = True
        template_type = 'network_connectivity_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ntp_policies(self):
        header = 'NTP Policy Variables'
        initial_policy = True
        template_type = 'ntp_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def port_policies(self):
        header = 'Port Policy Variables'
        initial_policy = True
        template_type = 'port_policies'

        # Set the org_count to 0 for the First Organization
        org_count = 0

        # Loop through the orgs discovered by the Class
        for org in self.orgs:

            # Pull in Variables from Class
            templateVars = self.templateVars
            templateVars['org'] = org

            # Define the Template Source
            templateVars['header'] = header
            templateVars['template_type'] = template_type
            template_file = "template_open.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            if initial_policy == True:
                write_method = 'w'
            else:
                write_method = 'a'
            process_method(write_method, dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = '%s.jinja2' % (template_type)
            template = self.templateEnv.get_template(template_file)

            if template_type in self.json_data['config']['orgs'][org_count]:
                for item in self.json_data['config']['orgs'][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars['org'] = org

                    # Define the Template Source
                    templateVars['header'] = header
                    for k, v in item.items():
                        if re.search(r'(_port_channels)', k):
                            templateVars[k] = []
                            attribute_list = {}
                            for i in v:
                                interface_list = []
                                for key, value in i.items():
                                    #if key == 'interfaces':
                                    #    for interfaces in value:
                                    #        int_dict = {}
                                    #        for keys, values in interfaces.items():
                                    #            if keys == 'aggr_id':
                                    #                int_dict.update({'breakout_port_id': values})
                                    #            elif keys == 'port_id':
                                    #                int_dict.update({'port_id': values})
                                    #            elif keys == 'slot_id':
                                    #                int_dict.update({'slot_id': values})
                                    #        x = copy.deepcopy(int_dict)
                                    #        interface_list.append(x)
                                    #        int_dict = {}
                                    # else:
                                    #     attribute_list.update({key: value})
                                    # attribute_list.update({'interfaces': interface_list})
                                    attribute_list.update({key: value})

                                attribute_list = dict(sorted(attribute_list.items()))
                                xdeep = copy.deepcopy(attribute_list)
                                templateVars[k].append(xdeep)
                                # print(k, templateVars[k])
                        elif re.search(r'(server_ports)', k):
                            aggr_ids = []
                            ports_count = 0
                            templateVars[k] = []
                            slot_ids = []
                            for i in v:
                                for key, value in i.items():
                                    if key == 'aggr_id':
                                        aggr_ids.append(value)
                                    if key == 'slot_id':
                                        slot_ids.append(value)
                            aggr_ids = list(set(aggr_ids))
                            slot_ids = list(set(slot_ids))
                            if len(aggr_ids) or len(slot_ids) > 1:
                                for i in v:
                                    attribute_list = {}
                                    port_list = []
                                    for key, value in i.items():
                                        if key == 'aggr_id':
                                            attribute_list.update({'breakout_port_id': value})
                                        elif key == 'port_id':
                                            port_list.append(value)
                                        else:
                                            attribute_list.update({'slot_id': value})
                                    attribute_list.update({'key_id': ports_count})
                                    attribute_list.update({'port_list': port_list})
                                    attribute_list = dict(sorted(attribute_list.items()))
                                    xdeep = copy.deepcopy(attribute_list)
                                    templateVars[k].append(xdeep)
                                    ports_count += 1
                            else:
                                attribute_list = {}
                                port_list = []
                                for i in v:
                                    for key, value in i.items():
                                        if key == 'aggr_id':
                                            attribute_list.update({'aggr_id': value})
                                        elif key == 'port_id':
                                            port_list.append(value)
                                        elif key == 'slot_id':
                                            attribute_list.update({'slot_id': value})
                                attribute_list.update({'key_id': ports_count})
                                ports_count += 1
                                port_list = ",".join("{0}".format(n) for n in port_list)
                                attribute_list.update({'port_list': port_list})
                                attribute_list = dict(sorted(attribute_list.items()))
                                xdeep = copy.deepcopy(attribute_list)
                                templateVars[k].append(xdeep)
                            # print(k, templateVars[k])
                        elif re.search(r'(san_unified_ports)', k):
                            for key, value in v.items():
                                if key == 'port_id_start':
                                    begin = value
                                elif key == 'port_id_end':
                                    end = value
                                elif key == 'slot_id':
                                    slot_id = value
                            templateVars['port_modes'] = {'port_list': [begin, end], 'slot_id': slot_id}
                        elif re.search(r'(_ports)$', k):
                            ports_count = 0
                            templateVars[k] = []
                            attribute_list = {}
                            for i in v:
                                for key, value in i.items():
                                    attribute_list.update({key: value})
                                attribute_list.update({'key_id': ports_count})
                                attribute_list = dict(sorted(attribute_list.items()))
                                xdeep = copy.deepcopy(attribute_list)
                                templateVars[k].append(xdeep)
                                ports_count += 1
                            # print(k, templateVars[k])
                        else:
                            templateVars[k] = v
                    if 'appliance_port_channels' in templateVars:
                        templateVars['port_channel_appliances'] = templateVars['appliance_port_channels']
                        del templateVars['appliance_port_channels']
                    if 'lan_port_channels' in templateVars:
                        templateVars['port_channel_ethernet_uplinks'] = templateVars['lan_port_channels']
                        del templateVars['lan_port_channels']
                    if 'san_port_channels' in templateVars:
                        templateVars['port_channel_fc_uplinks'] = templateVars['san_port_channels']
                        del templateVars['san_port_channels']
                        print(templateVars['port_channel_fc_uplinks'])
                    if 'fcoe_port_channels' in templateVars:
                        templateVars['port_channel_fcoe_uplinks'] = templateVars['fcoe_port_channels']
                        del templateVars['fcoe_port_channels']
                    if 'appliance_ports' in templateVars:
                        templateVars['port_role_appliances'] = templateVars['appliance_ports']
                        del templateVars['appliance_ports']
                    if 'lan_uplink_ports' in templateVars:
                        templateVars['port_role_ethernet_uplinks'] = templateVars['lan_uplink_ports']
                        del templateVars['lan_uplink_ports']
                    if 'san_uplink_ports' in templateVars:
                        templateVars['port_role_fc_uplinks'] = templateVars['san_uplink_ports']
                        del templateVars['san_uplink_ports']
                    if 'fcoe_uplink_ports' in templateVars:
                        templateVars['port_role_fcoe_uplinks'] = templateVars['fcoe_uplink_ports']
                        del templateVars['fcoe_uplink_ports']
                    if 'server_ports' in templateVars:
                        templateVars['port_role_servers'] = templateVars['server_ports']
                        del templateVars['server_ports']

                    templateVars = dict(sorted(templateVars.items()))
                    # print(templateVars)

                    # Process the template
                    dest_dir = '%s' % (self.type)
                    dest_file = '%s.auto.tfvars' % (template_type)
                    process_method('a', dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = "template_close.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            process_method('a', dest_dir, dest_file, template, **templateVars)

            # Increment the org_count for the next Organization Loop
            org_count += 1

    def power_policies(self):
        header = 'Power Policy Variables'
        initial_policy = True
        template_type = 'power_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def san_connectivity_policies(self):
        header = 'SAN Connectivity Policy Variables'
        initial_policy = True
        template_type = 'san_connectivity_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def sd_card_policies(self):
        header = 'SD Card Policy Variables'
        initial_policy = True
        template_type = 'sd_card_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def serial_over_lan_policies(self):
        header = 'Serial over LAN Policy Variables'
        initial_policy = True
        template_type = 'serial_over_lan_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def snmp_policies(self):
        header = 'SNMP Policy Variables'
        initial_policy = True
        template_type = 'snmp_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def storage_policies(self):
        header = 'Storage Policy Variables'
        initial_policy = True
        template_type = 'storage_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def switch_control_policies(self):
        header = 'Switch Control Policy Variables'
        initial_policy = True
        template_type = 'switch_control_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def syslog_policies(self):
        header = 'Syslog Policy Variables'
        initial_policy = True
        template_type = 'syslog_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def system_qos_policies(self):
        header = 'System QoS Policy Variables'
        initial_policy = True
        template_type = 'system_qos_policies'

        # Set the org_count to 0 for the First Organization
        org_count = 0

        # Loop through the orgs discovered by the Class
        for org in self.orgs:

            # Pull in Variables from Class
            templateVars = self.templateVars
            templateVars['org'] = org

            # Define the Template Source
            templateVars['header'] = header
            templateVars['template_type'] = template_type
            template_file = "template_open.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            if initial_policy == True:
                write_method = 'w'
            else:
                write_method = 'a'
            process_method(write_method, dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = '%s.jinja2' % (template_type)
            template = self.templateEnv.get_template(template_file)

            if template_type in self.json_data['config']['orgs'][org_count]:
                for item in self.json_data['config']['orgs'][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars['org'] = org

                    # Define the Template Source
                    templateVars['header'] = header

                    for k, v in item.items():
                        if (k == 'name' or k == 'descr' or k == 'tags'):
                            templateVars[k] = v

                templateVars['classes'] = []
                for r in range(0,6):
                    xdict = {}
                    templateVars['classes'].append(xdict)

                class_count = 0
                for item in self.json_data['config']['orgs'][org_count][template_type][0]['classes']:
                    for k, v in item.items():
                        templateVars['classes'][class_count][k] = v

                    class_count += 1

                total_weight = 0

                for r in range(0,6):
                    if templateVars['classes'][r]['state'] == 'Enabled':
                        total_weight += int(templateVars['classes'][r]['weight'])

                for r in range(0,6):
                    if templateVars['classes'][r]['state'] == 'Enabled':
                        x = ((int(templateVars['classes'][r]['weight']) / total_weight) * 100)
                        templateVars['classes'][r]['bandwidth_percent'] = str(x).split('.')[0]
                    else:
                        templateVars['classes'][r]['bandwidth_percent'] = 0

                # Process the template
                dest_dir = '%s' % (self.type)
                dest_file = '%s.auto.tfvars' % (template_type)
                process_method('a', dest_dir, dest_file, template, **templateVars)

            # Define the Template Source
            template_file = "template_close.jinja2"
            template = self.templateEnv.get_template(template_file)

            # Process the template
            dest_dir = '%s' % (self.type)
            dest_file = '%s.auto.tfvars' % (template_type)
            process_method('a', dest_dir, dest_file, template, **templateVars)

            # Increment the org_count for the next Organization Loop
            org_count += 1

    def thermal_policies(self):
        header = 'Thermal Policy Variables'
        initial_policy = True
        template_type = 'thermal_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ucs_domain_profiles(self):
        header = 'UCS Domain Profile Variables'
        initial_policy = True
        template_type = 'ucs_domain_profiles'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ucs_server_profiles(self):
        header = 'UCS Server Profile Variables'
        initial_policy = True
        template_type = 'ucs_server_profiles'

        policy_loop_standard(self, header, initial_policy, template_type)

    def ucs_server_profile_templates(self):
        header = 'UCS Server Profile Template Variables'
        initial_policy = True
        template_type = 'ucs_server_profile_templates'

        policy_loop_standard(self, header, initial_policy, template_type)

    def virtual_kvm_policies(self):
        header = 'Virtual KVM Policy Variables'
        initial_policy = True
        template_type = 'virtual_kvm_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def virtual_media_policies(self):
        header = 'Virtual Media Policy Variables'
        initial_policy = True
        template_type = 'virtual_media_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def vlan_policies(self):
        header = 'VLAN Policy Variables'
        initial_policy = True
        template_type = 'vlan_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def vsan_policies(self):
        header = 'VSAN Policy Variables'
        initial_policy = True
        template_type = 'vsan_policies'

        policy_loop_standard(self, header, initial_policy, template_type)

    def uuid_pools(self):
        header = 'UUID Pool Variables'
        initial_policy = True
        template_type = 'uuid_pools'

        policy_loop_standard(self, header, initial_policy, template_type)

    def wwnn_pools(self):
        header = 'Fibre Channel WWNN Pool Variables'
        initial_policy = True
        template_type = 'wwnn_pools'

        policy_loop_standard(self, header, initial_policy, template_type)

    def wwpn_pools(self):
        header = 'Fibre Channel WWPN Pool Variables'
        initial_policy = True
        template_type = 'wwpn_pools'

        policy_loop_standard(self, header, initial_policy, template_type)

class easy_imm_wizard(object):
    def __init__(self, name_prefix, org, type):
        self.templateLoader = jinja2.FileSystemLoader(
            searchpath=(ucs_template_path + '%s/') % (type))
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)
        self.name_prefix = name_prefix
        self.org = org
        self.type = type

    #========================================
    # BIOS Policy Module
    #========================================
    def bios_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_names = []
        policy_type = 'BIOS Policy'
        policy_x = 'BIOS'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['name_prefix'] = name_prefix
        templateVars['org'] = org
        templateVars['policy_file'] = 'bios_templates.txt'
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'bios_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'  {policy_x} Policies:  To simplify your work, this wizard will use {policy_x}')
        print(f'  Templates that are pre-configured.  You can add custom {policy_x} policy')
        print(f'  configuration to the {templateVars["template_type"]}.auto.tfvars file at your descretion.  ')
        print(f'  That will not be covered by this wizard as the focus of the wizard is on simplicity.')
        print(f'\n-------------------------------------------------------------------------------------------\n')

        templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
        policy_names = policy_template(self, **templateVars)

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Boot Order Policy Module
    #========================================
    def boot_order_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'boot_order'
        org = self.org
        policy_names = []
        policy_type = 'Boot Order Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'boot_order_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Ethernet Adapter Policy Module
    #========================================
    def ethernet_adapter_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_names = []
        policy_type = 'Ethernet Adapter Policy'
        policy_x = 'Ethernet Adapter'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['name_prefix'] = name_prefix
        templateVars['org'] = org
        templateVars['policy_file'] = 'ethernet_adapter_templates.txt'
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ethernet_adapter_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'  {policy_x} Policies:  To simplify your work, this wizard will use {policy_x}')
        print(f'  Templates that are pre-configured.  You can add custom {policy_x} policy')
        print(f'  configuration to the {templateVars["template_type"]}.auto.tfvars file at your descretion.  ')
        print(f'  That will not be covered by this wizard as the focus of the wizard is on simplicity.')
        print(f'\n-------------------------------------------------------------------------------------------\n')

        templateVars['template_file'] = 'ethernet_adapter_templates.jinja2'
        policy_names = policy_template(self, **templateVars)

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Ethernet Network Control Policy Module
    #========================================
    def ethernet_network_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'netwk_ctrl'
        org = self.org
        policy_names = []
        policy_type = 'Ethernet Network Control Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ethernet_network_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} will allow you to control Network Discovery with ')
            print(f'  protocols like CDP and LLDP as well as MAC Address Control Features.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars['action_on_uplink_fail'] = 'linkDown'

                    valid = False
                    while valid == False:
                        cdp = input('Do you want to enable CDP (Cisco Discovery Protocol) for this Policy?  Enter "Y" or "N" [Y]: ')
                        if cdp == '' or cdp == 'Y':
                            templateVars['cdp_enable'] = True
                            valid = True
                        elif cdp == 'N':
                            templateVars['cdp_enable'] = False
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        cdp = input('Do you want to enable LLDP (Link Level Discovery Protocol) for this Policy?  Enter "Y" or "N" [Y]: ')
                        if cdp == '' or cdp == 'Y':
                            templateVars['lldp_receive_enable'] = True
                            templateVars['lldp_transmit_enable'] = True
                            valid = True
                        elif cdp == 'N':
                            templateVars['lldp_receive_enable'] = False
                            templateVars['lldp_transmit_enable'] = False
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    templateVars['policy_file'] = 'mac_register_mode.txt'
                    templateVars['var_description'] = '   MAC Registration Mode:  Default is "nativeVlanOnly".\n   Determines the MAC addresses that have to be registered with the switch.'
                    templateVars["var_type"] = 'MAC Registration Mode'
                    templateVars["mac_register_mode"] = variable_loop(**templateVars)

                    templateVars['policy_file'] = 'mac_security_forge.txt'
                    templateVars['var_description'] = '   MAC Security Forge:  Default is "allow".\n   Determines if the MAC forging is allowed or denied on an interface.'
                    templateVars["var_type"] = 'MAC Security Forge'
                    templateVars["mac_security_forge"] = variable_loop(**templateVars)

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Ethernet Network Group Policy Module
    #========================================
    def ethernet_network_group_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vlan_group'
        org = self.org
        policy_names = []
        policy_type = 'Ethernet Network Group Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ethernet_network_group_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} will define the Allowed VLANs on a Server vNIC Template.')
            print(f'  As a recommendation you will need an {policy_type} per vNIC Group.')
            print(f'  For Instance with a Virtual Host that may have the following vNIC Groups:')
            print(f'     1. Management')
            print(f'     2. Migration/vMotion')
            print(f'     3. Storage')
            print(f'     4. Virtual Machines')
            print(f'  You will want to configure 1 {policy_type} per Group.')
            print(f'  The allowed vlan list can be in the format of:')
            print(f'     5 - Single VLAN')
            print(f'     1-10 - Range of VLANs')
            print(f'     1,2,3,4,5,11,12,13,14,15 - List of VLANs')
            print(f'     1-10,20-30 - Ranges and Lists of VLANs')
            print(f'  If you want to Assign a Native VLAN Make sure it is in the allowed list.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars['action_on_uplink_fail'] = 'linkDown'

                    valid = False
                    while valid == False:
                        vlan_list = input('Enter the VLAN or List of VLANs to add to this VLAN Group: ')
                        if not vlan_list == '':
                            vlan_list_expanded = vlan_list_full(vlan_list)
                            valid_vlan = True
                            for vlan in vlan_list_expanded:
                                valid_vlan = validating_ucs.number_in_range('VLAN ID', vlan, 1, 4094)
                                if valid_vlan == False:
                                    break
                            native_count = 0
                            native_vlan = ''
                            if valid_vlan == True:
                                native_vlan = input('If you want to configure one of the VLANs as a Native VLAN in this list add it here. [press enter to skip]:')
                            if not native_vlan == '' and valid_vlan == True:
                                for vlan in vlan_list_expanded:
                                    if int(native_vlan) == int(vlan):
                                        native_count = 1
                                if native_count == 1:
                                    valid = True
                                else:
                                    print(f'\n---------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The Native VLAN was not in the Allowed List.')
                                    print(f'\n---------------------------------------------------------------------------------------\n')

                            elif valid_vlan == True:
                                valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  The allowed vlan list can be in the format of:')
                            print(f'     5 - Single VLAN')
                            print(f'     1-10 - Range of VLANs')
                            print(f'     1,2,3,4,5,11,12,13,14,15 - List of VLANs')
                            print(f'     1-10,20-30 - Ranges and Lists of VLANs')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    templateVars['allowed_vlans'] = vlan_list
                    if not native_vlan == '':
                        templateVars['native_vlan'] = native_vlan

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Ethernet Network Policy Module
    #========================================
    def ethernet_network_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'netwk'
        org = self.org
        policy_names = []
        policy_type = 'Ethernet Network Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ethernet_network_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Ethernet QoS Policy Module
    #========================================
    def ethernet_qos_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'qos'
        org = self.org
        policy_names = []
        policy_type = 'Ethernet QoS Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ethernet_qos_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} will configure QoS on a Server vNIC Template.')
            print(f'  As a recommendation you will need an {policy_type} per vNIC Group.')
            print(f'  For Instance with a Virtual Host that may have the following vNIC Groups:')
            print(f'     1. Management')
            print(f'     2. Migration/vMotion')
            print(f'     3. Storage')
            print(f'     4. Virtual Machines')
            print(f'  It would be a best practice to configure different QoS Priorities for Each Network.')
            print(f'  For Instance a good practice would be something like the following:')
            print(f'     Management - Silver')
            print(f'     Migration/vMotion - Bronze')
            print(f'     Storage - Platinum')
            print(f'     Virtual Machines - Gold.')
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars["burst"] = 1024
                    templateVars["enable_trust_host_cos"] = False
                    templateVars["rate_limit"] = 0

                    valid = False
                    while valid == False:
                        mtu = input('Do you want to enable Jumbo MTU?  Enter "Y" or "N" [Y]: ')
                        if mtu == '' or mtu == 'Y':
                            templateVars['mtu'] = 9216
                            valid = True
                        elif mtu == 'N':
                            templateVars['mtu'] = 1500
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    templateVars['policy_file'] = 'qos_priority.txt'
                    templateVars['var_description'] = '   Priority:  Default is "Best Effort".\n   The priortity matching the System QoS specified in the fabric profile.'
                    templateVars["var_type"] = 'Priority'
                    templateVars["priority"] = variable_loop(**templateVars)

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Fibre-Channel Adapter Policy Module
    #========================================
    def fibre_channel_adapter_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_names = []
        policy_type = 'Fibre-Channel Adapter Policy'
        policy_x = 'Fibre-Channel Adapter'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['name_prefix'] = name_prefix
        templateVars['org'] = org
        templateVars['policy_file'] = 'fibre_channel_adapter_templates.txt'
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'fibre_channel_adapter_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'  {policy_x} Policies:  To simplify your work, this wizard will use {policy_x}')
        print(f'  Templates that are pre-configured.  You can add custom {policy_x} policy')
        print(f'  configuration to the {templateVars["template_type"]}.auto.tfvars file at your descretion.  ')
        print(f'  That will not be covered by this wizard as the focus of the wizard is on simplicity.')
        print(f'  Skip if you are not configuring Fibre-Channel.')
        print(f'\n-------------------------------------------------------------------------------------------\n')

        templateVars['template_file'] = 'ethernet_adapter_templates.jinja2'
        policy_names = policy_template(self, **templateVars)

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Fibre-Channel Network Policy Module
    #========================================
    def fibre_channel_network_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_names = []
        policy_type = 'Fibre-Channel Network Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'fibre_channel_network_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  Fibre-Channel Network Policies Notes:')
            print(f'  - You will need one Policy per Fabric.  VSAN A / VSAN B.')
            print(f'  - Skip if you are not configuring Fibre-Channel.')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - UCS/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 1
                policy_loop = False
                while policy_loop == False:

                    name = naming_rule_fabric(loop_count, name_prefix, org)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars['default_vlan'] = 0

                    valid = False
                    while valid == False:
                        if loop_count % 2 == 0:
                            templateVars['vsan_id'] = input('What VSAN Do you want to Assign to this Policy?  [200]: ')
                        else:
                            templateVars['vsan_id'] = input('What VSAN Do you want to Assign to this Policy?  [100]: ')
                        if templateVars['vsan_id'] == '':
                            if loop_count % 2 == 0:
                                templateVars['vsan_id'] = 200
                            else:
                                templateVars['vsan_id'] = 100
                        valid = validating_ucs.number_in_range('VSAN ID', templateVars['vsan_id'], 1, 4094)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'   name        = "{templateVars["name"]}"')
                    print(f'   description = "{templateVars["descr"]}"')
                    print(f'   vsan_id     = "{templateVars["vsan_id"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'
                        # Write Policies to Template File
                        templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                        write_to_template(self, **templateVars)

                        # Add Template Name to Policies Output
                        policy_names.append(templateVars['name'])

                        exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
                        if exit_answer == 'N':
                            policy_loop = True
                            configure_loop = True
                        loop_count += 1
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Starting Section over')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Fibre-Channel QoS Policy Module
    #========================================
    def fibre_channel_qos_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'qos'
        org = self.org
        policy_names = []
        policy_type = 'Fibre-Channel QoS Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'fibre_channel_qos_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  It is a good practice to apply a {policy_type} to the vHBAs.  This wizard')
            print(f'  creates the policy with all the default values, so you only need one')
            print(f'  {policy_type}.  Skip if you are not configuring Fibre-Channel.')
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars['burst'] = 1024
                    templateVars['max_data_field_size'] = 2112
                    templateVars['rate_limit'] = 0

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Firmware - UCS Domain Module
    #========================================
    def firmware_ucs_domain(self):
        templateVars = {}
        templateVars['header'] = 'UCS Domain Profile Variables'
        templateVars['initial_write'] = True
        templateVars['org'] = self.org
        templateVars['policy_type'] = 'UCS Domain Profile'
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ntp_policies'
        valid = False
        while valid == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            print(f'   UCS Version of Software to Deploy...')
            if os.path.isfile('ucs_version.txt'):
                version_file = open('ucs_version.txt', 'r')
                versions = []
                for line in version_file:
                    line = line.strip()
                    versions.append(line)
                for i, v in enumerate(versions):
                    i += 1
                    if i < 10:
                        print(f'     {i}. {v}')
                    else:
                        print(f'    {i}. {v}')
            print(f'\n---------------------------------------------------------------------------------------\n')
            ucs_version = input('Enter the Index Number for the Version of Software to Run: ')
            for i, v in enumerate(versions):
                i += 1
                if int(ucs_version) == i:
                    ucs_domain_version = v
                    valid = True
            if valid == False:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                print(f'\n---------------------------------------------------------------------------------------\n')
            version_file.close()

    #========================================
    # Flow Control Policy Module
    #========================================
    def flow_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'flow_ctrl'
        org = self.org
        policy_names = []
        policy_type = 'Flow Control Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'flow_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # IMC Access Policy Module
    #========================================
    def imc_access_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'imc_access'
        org = self.org
        policy_names = []
        policy_type = 'IMC Access Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'imc_access_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # IP Pools Module
    #========================================
    def ip_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'ip_pool'
        org = self.org
        policy_names = []
        policy_type = 'IP Pool'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ip_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'    At a minimum you will need one IP Pool for KVM Access to Servers.  This will be an ')
            print(f'    inband VLAN assigned through the domain.')
            print(f'    Currently out-of-band mgmt is not supported in IMM for KVM access.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the number for the value to select.  [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        config_ipv4 = input('Do you want to configure IPv4 for this Pool?  Enter "Y" or "N" [Y]: ')
                        if config_ipv4 == 'Y' or config_ipv4 == '':
                            valid = True
                        elif config_ipv4 == 'N':
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    if config_ipv4 == 'Y' or config_ipv4 == '':
                        valid = False
                        while valid == False:
                            network_prefix = input('What is the Gateway/Mask to Assign to the Pool?  [198.18.0.1/24]: ')
                            if network_prefix == '':
                                network_prefix = '198.18.0.1/24'
                            gateway_valid = validating_ucs.ip_address('Gateway Address', network_prefix)
                            mask_valid = validating_ucs.number_in_range('Mask Length', network_prefix.split('/')[1], 1, 30)
                            if gateway_valid == True and mask_valid == True:
                                valid = True
                            else:
                                print(f'\n---------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please Verify you have entered the gateway/prefix correctly.')
                                print(f'\n---------------------------------------------------------------------------------------\n')

                        gateway = str(ipaddress.IPv4Interface(network_prefix).ip)
                        netmask = str(ipaddress.IPv4Interface(network_prefix).netmask)
                        network = str(ipaddress.IPv4Interface(network_prefix).network)
                        prefix = network_prefix.split('/')[1]

                        valid = False
                        while valid == False:
                            starting = input('What is the Starting IP Address to Assign to the Pool?  [198.18.0.10]: ')
                            if starting == '':
                                starting = '198.18.0.10'
                            valid_ip = validating_ucs.ip_address('Starting IP Address', starting)
                            if valid_ip == True:
                                if network == str(ipaddress.IPv4Interface('/'.join([starting, prefix])).network):
                                    valid = True
                                else:
                                    print(f'\n---------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please Verify the starting IP is in the same network')
                                    print(f'  as the Gateway')
                                    print(f'\n---------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            pool_size = input('How Many IP Addresses should be added to the Pool?  Range is 1-1000 [160]: ')
                            if pool_size == '':
                                pool_size = '160'
                            valid = validating_ucs.number_in_range('Pool Size', pool_size, 1, 1000)

                        valid = False
                        while valid == False:
                            primary_dns = input('What is your Primary DNS Server [208.67.220.220]? ')
                            if primary_dns == '':
                                primary_dns = '208.67.220.220'
                            valid = validating_ucs.ip_address('Primary DNS Server', primary_dns)

                        valid = False
                        while valid == False:
                            alternate_true = input('Do you want to Configure an Alternate DNS Server?  Enter "Y" or "N" [Y]: ')
                            if alternate_true == 'Y' or alternate_true == '':
                                secondary_dns = input('What is your Alternate DNS Server [208.67.222.222]? ')
                                if secondary_dns == '':
                                    secondary_dns = '208.67.222.222'
                                valid = validating_ucs.ip_address('Alternate DNS Server', secondary_dns)
                            elif alternate_true == 'N':
                                secondary_dns = ''
                                valid = True
                            else:
                                print(f'\n---------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n---------------------------------------------------------------------------------------\n')

                        beginx = int(ipaddress.IPv4Address(starting))
                        add_dec = (beginx + int(pool_size))
                        ending = str(ipaddress.IPv4Address(add_dec))

                        templateVars['ipv4_blocks'] = [{'from':starting, 'to':ending}]
                        templateVars['ipv4_configuration'] = {'gateway':gateway, 'netmask':netmask,
                            'primary_dns':primary_dns, 'secondary_dns':secondary_dns}

                    valid = False
                    while valid == False:
                        config_ipv4 = input('Do you want to configure IPv6 for this Pool?  Enter "Y" or "N" [Y]: ')
                        if config_ipv4 == 'Y' or config_ipv4 == '':
                            valid = True
                        elif config_ipv4 == 'N':
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    if config_ipv4 == 'Y' or config_ipv4 == '':
                        valid = False
                        while valid == False:
                            network_prefix = input('What is the Gateway/Mask to Assign to the Pool?  [2001:0002::1/64]: ')
                            if network_prefix == '':
                                network_prefix = '2001:0002::1/64'
                            gateway_valid = validating_ucs.ip_address('Gateway Address', network_prefix)
                            mask_valid = validating_ucs.number_in_range('Mask Length', network_prefix.split('/')[1], 48, 127)
                            if gateway_valid == True and mask_valid == True:
                                valid = True
                            else:
                                print(f'\n---------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please Verify you have entered the gateway/prefix correctly.')
                                print(f'\n---------------------------------------------------------------------------------------\n')

                        # broadcast = str(ipaddress.IPv4Interface(network_prefix).broadcast_address)
                        gateway = str(ipaddress.IPv6Interface(network_prefix).ip)
                        network = str(ipaddress.IPv6Interface(network_prefix).network)
                        prefix = network_prefix.split('/')[1]

                        valid = False
                        while valid == False:
                            starting = input('What is the Starting IP Address to Assign to the Pool?  [2001:0002::10]: ')
                            if starting == '':
                                starting = '2001:0002::10'
                            valid_ip = validating_ucs.ip_address('Starting IP Address', starting)
                            if valid_ip == True:
                                if network == str(ipaddress.IPv6Interface('/'.join([starting, prefix])).network):
                                    valid = True
                                    # print('gateway and starting ip are in the same network')
                                else:
                                    print(f'\n---------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please Verify the starting IP is in the same network')
                                    print(f'  as the Gateway')
                                    print(f'\n---------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            pool_size = input('How Many IP Addresses should be added to the Pool?  Range is 1-1000 [160]: ')
                            if pool_size == '':
                                pool_size = '160'
                            valid = validating_ucs.number_in_range('Pool Size', pool_size, 1, 1000)

                        valid = False
                        while valid == False:
                            primary_dns = input('What is your Primary DNS Server [2620:119:35::35]? ')
                            if primary_dns == '':
                                primary_dns = '2620:119:35::35'
                            valid = validating_ucs.ip_address('Primary DNS Server', primary_dns)

                        valid = False
                        while valid == False:
                            alternate_true = input('Do you want to Configure an Alternate DNS Server? Enter "Y" or "N" [Y]: ')
                            if alternate_true == 'Y' or alternate_true == '':
                                secondary_dns = input('What is your Alternate DNS Server [2620:119:53::53]? ')
                                if secondary_dns == '':
                                    secondary_dns = '2620:119:53::53'
                                valid = validating_ucs.ip_address('Alternate DNS Server', secondary_dns)
                            elif alternate_true == 'N':
                                secondary_dns = ''
                                valid = True
                            else:
                                print(f'\n---------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n---------------------------------------------------------------------------------------\n')

                        # beginx = int(ipaddress.IPv6Address(starting))
                        # add_dec = (beginx + int(pool_size))
                        # ending = str(ipaddress.IPv6Address(add_dec))

                        templateVars['ipv6_blocks'] = [{'from':starting, 'size':pool_size}]
                        templateVars['ipv6_configuration'] = {'gateway':gateway, 'prefix':prefix,
                            'primary_dns':primary_dns, 'secondary_dns':secondary_dns}

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # IPMI over LAN Policy Module
    #========================================
    def ipmi_over_lan_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ipmi'
        org = self.org
        policy_names = []
        policy_type = 'IPMI over LAN Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ipmi_over_lan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # IQN Pools Module
    #========================================
    def iqn_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'iqn_pool'
        org = self.org
        policy_names = []
        policy_type = 'IQN Pool'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'iqn_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # iSCSI Adapter Policy Module
    #========================================
    def iscsi_adapter_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'adapter'
        org = self.org
        policy_names = []
        policy_type = 'iSCSI Adapter Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'iscsi_adapter_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # iSCSI Boot Policy Module
    #========================================
    def iscsi_boot_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'boot'
        org = self.org
        policy_names = []
        policy_type = 'iSCSI Boot Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'iscsi_boot_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the Index for the value to select [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # iSCSI Static Target Policy Module
    #========================================
    def iscsi_static_target_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'target'
        org = self.org
        policy_names = []
        policy_type = 'iSCSI Static Target Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'iscsi_static_target_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # LAN Connectivity Policy Module
    #========================================
    def lan_connectivity_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'lan'
        org = self.org
        policy_names = []
        policy_type = 'LAN Connectivity Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'lan_connectivity_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Link Aggregation Policy Module
    #========================================
    def link_aggregation_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'link_agg'
        org = self.org
        policy_names = []
        policy_type = 'Link Aggregation Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'link_aggregation_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['lacp_rate'] = 'normal'
                    templateVars['suspend_individual'] = False

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Link Control Policy Module
    #========================================
    def link_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'link_ctrl'
        org = self.org
        policy_names = []
        policy_type = 'Link Control Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'link_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['admin_state'] = 'Enabled'
                    templateVars['mode'] = 'normal'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # MAC Pools Module
    #========================================
    def mac_pools(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_names = []
        policy_type = 'MAC Pool'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'mac_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  MAC Pool Convention Recommendations:')
            print(f'  - Leverage the Cisco UCS OUI of 00:25:B5 for the MAC Pool Prefix.')
            print(f'  - For MAC Pools; create a pool for each Fabric.')
            print(f'  - Pool Size can be between 1 and 1000 addresses.')
            print(f'  - Refer to "UCS Naming Conventions 0.5.ppsx" in the Repository for further guidance.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 1
                policy_loop = False
                while policy_loop == False:

                    name = naming_rule_fabric(loop_count, name_prefix, org)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the number for the value to select.  [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        if loop_count % 2 == 0:
                            begin = input('What is the Beginning MAC Address to Assign to the Pool?  [00:25:B5:0B:00:00]: ')
                        else:
                            begin = input('What is the Beginning MAC Address to Assign to the Pool?  [00:25:B5:0A:00:00]: ')
                        if begin == '':
                            if loop_count % 2 == 0:
                                begin = '00:25:B5:0B:00:00'
                            else:
                                begin = '00:25:B5:0A:00:00'
                        valid = validating_ucs.mac_address('MAC Pool Address', begin)

                    valid = False
                    while valid == False:
                        pool_size = input('How Many Mac Addresses should be added to the Pool?  Range is 1-1000 [512]: ')
                        if pool_size == '':
                            pool_size = '512'
                        valid = validating_ucs.number_in_range('Pool Size', pool_size, 1, 1000)

                    begin = begin.upper()
                    beginx = int(begin.replace(':', ''), 16)
                    add_dec = (beginx + int(pool_size))
                    ending = ':'.join(['{}{}'.format(a, b)
                        for a, b
                        in zip(*[iter('{:012x}'.format(add_dec))]*2)])
                    ending = ending.upper()
                    templateVars['mac_blocks'] = [{'from':begin, 'to':ending}]

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
                    if exit_answer == 'N':
                        policy_loop = True
                        configure_loop = True
                    loop_count += 1
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Multicast Policy Module
    #========================================
    def multicast_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'multicast'
        org = self.org
        policy_names = []
        policy_type = 'Multicast Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'multicast_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            print(f"  You must Create at least one Multicast Policy; each VLAN must have a Multicast Policy")
            print(f"  applied to it.  Optional attributes will be the IGMP Querier IP's.  IGMP Querier")
            print(f"  IP's are only needed if you have a non Routed VLAN and you need the Fabric")
            print(f"  Interconnects to act as IGMP Querier's for the network.")
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars['igmp_snooping_state'] = 'Enabled'

                    valid = False
                    while valid == False:
                        print(f'\n---------------------------------------------------------------------------------------\n')
                        templateVars['querier_ip_address'] = input('IGMP Querier IP for Fabric Interconnect A.  [press enter to skip] ')
                        if templateVars['querier_ip_address'] == '':
                            valid = True
                        if not templateVars['querier_ip_address'] == '':
                            valid = validating_ucs.ip_address('Fabric A IGMP Querier IP', templateVars['querier_ip_address'])

                        if not templateVars['querier_ip_address'] == '':
                            templateVars['igmp_snooping_querier_state'] == 'Enabled'
                            valid = False
                            while valid == False:
                                print(f'\n---------------------------------------------------------------------------------------\n')
                                templateVars['querier_ip_address_peer'] = input('IGMP Querier IP for Fabric Interconnect B.  [press enter to skip] ')
                                if templateVars['querier_ip_address_peer'] == '':
                                    valid = True
                                if not templateVars['querier_ip_address_peer'] == '':
                                    valid = validating_ucs.ip_address('Fabric B IGMP Querier IP', templateVars['querier_ip_address'])
                        else:
                            templateVars['igmp_snooping_querier_state'] == 'Disabled'
                            templateVars['querier_ip_address_peer'] == ''

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Network Connectivity Policy Module
    #========================================
    def network_connectivity_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'dns'
        org = self.org
        policy_names = []
        policy_type = 'Network Connectivity Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'network_connectivity_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    valid = False
                    while valid == False:
                        print(f'\n---------------------------------------------------------------------------------------\n')
                        templateVars['preferred_ipv4_dns_server'] = input('What is your Primary IPv4 DNS Server [208.67.220.220]? ')
                        if templateVars['preferred_ipv4_dns_server'] == '':
                            templateVars['preferred_ipv4_dns_server'] = '208.67.220.220'
                        valid = validating_ucs.ip_address('Primary IPv4 DNS Server', templateVars['preferred_ipv4_dns_server'])

                    valid = False
                    while valid == False:
                        alternate_true = input('Do you want to Configure an Alternate IPv4 DNS Server [Y/N]? ')
                        if alternate_true == 'Y':
                            templateVars['alternate_ipv4_dns_server'] = input('What is your Alternate IPv4 DNS Server [208.67.222.222]? ')
                            if templateVars['alternate_ipv4_dns_server'] == '':
                                templateVars['alternate_ipv4_dns_server'] = '208.67.222.222'
                            valid = validating_ucs.ip_address('Alternate IPv4 DNS Server', templateVars['alternate_ipv4_dns_server'])
                        elif alternate_true == 'N':
                            templateVars['alternate_ipv4_dns_server'] = ''
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        enable_ipv6 = input('Do you want to Configure IPv6 DNS [Y/N]? ')
                        if enable_ipv6 == 'Y':
                            templateVars['enable_ipv6'] = True
                            templateVars['preferred_ipv6_dns_server'] = input('What is your Primary IPv6 DNS Server [2620:119:35::35]? ')
                            if templateVars['preferred_ipv6_dns_server'] == '':
                                templateVars['preferred_ipv6_dns_server'] = '2620:119:35::35'
                            valid = validating_ucs.ip_address('Primary IPv6 DNS Server', templateVars['preferred_ipv6_dns_server'])
                        if enable_ipv6 == 'N':
                            templateVars['enable_ipv6'] = False
                            templateVars['preferred_ipv6_dns_server'] = ''
                            valid = True

                    valid = False
                    while valid == False:
                        if enable_ipv6 == 'Y':
                            alternate_true = input('Do you want to Configure an Alternate IPv6 DNS Server [Y/N]? ')
                            if alternate_true == 'Y':
                                templateVars['alternate_ipv6_dns_server'] = input('What is your Alternate IPv6 DNS Server [2620:119:53::53]? ')
                                if templateVars['alternate_ipv6_dns_server'] == '':
                                    templateVars['alternate_ipv6_dns_server'] = '2620:119:53::53'
                                valid = validating_ucs.ip_address('Alternate IPv6 DNS Server', templateVars['alternate_ipv6_dns_server'])
                            elif alternate_true == 'N':
                                templateVars['alternate_ipv6_dns_server'] = ''
                                valid = True
                            else:
                                print(f'\n---------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n---------------------------------------------------------------------------------------\n')
                        else:
                            templateVars['alternate_ipv6_dns_server'] = ''
                            valid = True

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # NTP Policy Module
    #========================================
    def ntp_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ntp'
        org = self.org
        policy_names = []
        policy_type = 'NTP Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_file'] = 'timezones.txt'
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ntp_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    valid = False
                    while valid == False:
                        primary_ntp = input('What is your Primary NTP Server [0.north-america.pool.ntp.org]: ')
                        if primary_ntp == "":
                            primary_ntp = '0.north-america.pool.ntp.org'
                        if re.search(r'[a-zA-Z]+', primary_ntp):
                            valid = validating_ucs.dns_name('Primary NTP Server', primary_ntp)
                        else:
                            valid = validating_ucs.ip_address('Primary NTP Server', primary_ntp)

                    valid = False
                    while valid == False:
                        alternate_true = input('Do you want to Configure an Alternate NTP Server [Y/N]? ')
                        if alternate_true == 'Y':
                            alternate_ntp = input('What is your Alternate NTP Server [1.north-america.pool.ntp.org]? ')
                            if alternate_ntp == "":
                                alternate_ntp = '1.north-america.pool.ntp.org'
                            if re.search(r'[a-zA-Z]+', alternate_ntp):
                                valid = validating_ucs.dns_name('Alternate NTP Server', alternate_ntp)
                            else:
                                valid = validating_ucs.ip_address('Alternate NTP Server', alternate_ntp)
                        elif alternate_true == 'N':
                            alternate_ntp = ''
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    templateVars['enabled'] = True
                    templateVars['ntp_servers'] = []
                    templateVars['ntp_servers'].append(primary_ntp)
                    if alternate_true == 'Y':
                        templateVars['ntp_servers'].append(alternate_ntp)

                    valid = False
                    while valid == False:
                        print(f'\n---------------------------------------------------------------------------------------')
                        print(f'   Timezone Regions...')
                        policy_file = 'ucs_templates/variables/%s' % (templateVars['policy_file'])
                        if os.path.isfile(policy_file):
                            template_file = open(policy_file, 'r')
                            tz_regions = []
                            for line in template_file:
                                tz_region = line.split('/')[0]
                                if not tz_region in tz_regions:
                                    tz_regions.append(tz_region)
                            for index, value in enumerate(tz_regions):
                                index += 1
                                if index < 10:
                                    print(f'     {index}. {value}')
                                else:
                                    print(f'    {index}. {value}')
                        print(f'---------------------------------------------------------------------------------------\n')
                        time_region = input('Please Enter the Index for the Time Region for the Domain: ')
                        for index, value in enumerate(tz_regions):
                            index += 1
                            if int(time_region) == index:
                                valid = True
                        if valid == False:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        print(f'\n---------------------------------------------------------------------------------------')
                        print(f'   Region Timezones...')
                        for index, value in enumerate(tz_regions):
                            index += 1
                            if int(time_region) == index:
                                tz_region = value
                                region_tzs = []
                                template_file.seek(0)
                                for line in template_file:
                                    if tz_region in line:
                                        line = line.strip()
                                        region_tzs.append(line)
                                for i, v in enumerate(region_tzs):
                                    i += 1
                                    if i < 10:
                                        print(f'     {i}. {v}')
                                    else:
                                        print(f'    {i}. {v}')
                        print(f'---------------------------------------------------------------------------------------\n')
                        timezone_index = input('Please Enter the Index for the Region Timezone to assign to the Domain: ')
                        for i, v in enumerate(region_tzs):
                            i += 1
                            if int(timezone_index) == i:
                                templateVars['timezone'] = v
                                valid = True
                        if valid == False:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')
                        template_file.close()

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Port Policy Module
    #========================================
    def port_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ports'
        org = self.org
        policy_names = []
        policy_type = 'Port Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'port_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Power Policy Module
    #========================================
    def power_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'power'
        org = self.org
        policy_names = []
        policy_type = 'Power Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'power_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # SAN Connectivity Policy Module
    #========================================
    def san_connectivity_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'san'
        org = self.org
        policy_names = []
        policy_type = 'SAN Connectivity Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'san_connectivity_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # SD Card Policy Module
    #========================================
    def sd_card_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'sdcard'
        org = self.org
        policy_names = []
        policy_type = 'SD Card Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'sd_card_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Serial over LAN Policy Module
    #========================================
    def serial_over_lan_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'sol'
        org = self.org
        policy_names = []
        policy_type = 'Serial over LAN Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'serial_over_lan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # SNMP Policy Module
    #========================================
    def snmp_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'snmp'
        org = self.org
        policy_names = []
        policy_type = 'SNMP Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'snmp_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Storage Policy Module
    #========================================
    def storage_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'storage'
        org = self.org
        policy_names = []
        policy_type = 'Storage Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'storage_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Switch Control Policy Module
    #========================================
    def switch_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'sw_ctrl'
        org = self.org
        policy_names = []
        policy_type = 'Switch Control Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'switch_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['mac_address_table_aging'] = 'Default'
                    templateVars['vlan_port_count_optimization'] = False

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Syslog Policy Module
    #========================================
    def syslog_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'syslog'
        org = self.org
        policy_names = []
        policy_type = 'Syslog Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'syslog_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # System QoS Policy Module
    #========================================
    def system_qos_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'link_ctrl'
        org = self.org
        policy_names = []
        policy_type = 'System QoS Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'system_qos_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['admin_state'] = 'Enabled'
                    templateVars['mode'] = 'normal'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Thermal Policy Module
    #========================================
    def thermal_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'thermal'
        org = self.org
        policy_names = []
        policy_type = 'Thermal Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'thermal_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # UCS Domain Profile Module
    #========================================
    def ucs_domain_profiles(self, **policies):
        name_prefix = self.name_prefix
        name_suffix = 'ucs'
        org = self.org
        policy_type = 'UCS Domain Profile'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'ucs_domain_profiles'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s' % (name_prefix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    valid = False
                    while valid == False:
                        print(f'\n---------------------------------------------------------------------------------------\n')
                        print(f'  1. UCS-FI-6454')
                        print(f'  2. UCS-FI-64108')
                        print(f'\n---------------------------------------------------------------------------------------\n')
                        model = input('Select the Index Value of the model of the Fabric Interconnects: ')
                        if model == '1':
                            templateVars['device_model'] = 'UCS-FI-6454'
                            valid = True
                        elif model == '2':
                            templateVars['device_model'] = 'UCS-FI-64108'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        print(f'\n---------------------------------------------------------------------------------------\n')
                        print(f'  Note: If you do not have the Serial Number at this time you can manually')
                        print(f'        add it to the ucs_domain_profiles/ucs_domain_profile.auto.tfvars')
                        print(f'        file later.')
                        print(f'\n---------------------------------------------------------------------------------------\n')
                        templateVars['serial_number_fabric_a'] = input('What is the Serial Number of Fabric A [press enter to skip]? ')
                        templateVars['serial_number_fabric_b'] = input('What is the Serial Number of Fabric B [press enter to skip]? ')
                        valid = True

                    policy_list = [
                        'network_connectivity_policies',
                        'ntp_policies',
                        # 'snmp_policies',
                        'switch_control_policies',
                        # 'syslog_policies',
                        # 'system_qos_policies'
                    ]
                    for policy in policy_list:
                        policy_short = policy.replace('policies', 'policy')
                        x = policy_short.split('_')
                        policy_description = []
                        for y in x:
                            y = y.capitalize()
                            policy_description.append(y)
                        policy_description = " ".join(policy_description)
                        policy_description = policy_description.replace('Ntp', 'NTP')
                        policy_description = policy_description.replace('Snmp', 'SNMP')

                        if len(policy) > 0:
                            templateVars['policy'] = policy_description
                            templateVars[policy_short] = policies_list(policies.get(policy), **templateVars)
                        else:
                            templateVars[policy_short] = ""

                    policy_list = [
                        # 'port_policies',
                        # 'vlan_policies',
                        # 'vsan_policies'
                    ]
                    for policy in policy_list:
                        policy_short = policy.replace('policies', 'policy')
                        x = policy_short.split('_')
                        policy_description = []
                        for y in x:
                            y = y.capitalize()
                            policy_description.append(y)
                        policy_description = " ".join(policy_description)

                        templateVars[policy] = {}
                        if len(policy) > 0:
                            templateVars['policy'] = '%s Fabric A' % (policy_description)
                            templateVars[policy]['fabric_a'] = policies_list(policies.get(policy), **templateVars)
                            templateVars['policy'] = '%s Fabric B' % (policy_description)
                            templateVars[policy]['fabric_b'] = policies_list(policies.get(policy), **templateVars)
                        else:
                            templateVars[policy]['fabric_a'] = ""
                            templateVars[policy]['fabric_b'] = ""

                    # Write Policies to Template File
                    # templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    # write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # UUID Pools Module
    #========================================
    def uuid_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'uuid_pool'
        org = self.org
        policy_names = []
        policy_type = 'UUID Pool'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'uuid_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Virtual KVM Policy Module
    #========================================
    def virtual_kvm_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vkvm'
        org = self.org
        policy_names = []
        policy_type = 'Virtual KVM Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'virtual_kvm_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # Virtual Media Policy Module
    #========================================
    def virtual_media_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vmedia'
        org = self.org
        policy_names = []
        policy_type = 'Virtual Media Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'virtual_media_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # VLAN Policy Module
    #========================================
    def vlan_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vlans'
        org = self.org
        policy_names = []
        policy_type = 'VLAN Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'vlan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will define the VLANs Assigned to the Fabric Interconnects.')
            print(f'  The vlan list can be in the format of:')
            print(f'     5 - Single VLAN')
            print(f'     1-10 - Range of VLANs')
            print(f'     1,2,3,4,5,11,12,13,14,15 - List of VLANs')
            print(f'     1-10,20-30 - Ranges and Lists of VLANs')
            print(f'  When configuring a VLAN List or Range the name will be used as a prefix in the format of:')
            print('     {name}-vlXXXX')
            print(f'  Where XXXX would be 0001 for vlan 1, 0100 for vlan 100, and 4094 for vlan 4094.')
            print(f'  If you want to Assign a Native VLAN Make sure it is in the vlan list for this wizard.')
            print(f'  IMPORTANT NOTE: You can only have one Native VLAN for the Fabric at this time,')
            print(f'                  as Disjoint Layer 2 is not yet supported.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)
                    templateVars['auto_allow_on_uplinks'] = True

                    valid = False
                    while valid == False:
                        vlan_list = input('Enter the VLAN or List of VLANs to add to this Name/Prefix Grouping: ')
                        if not vlan_list == '':
                            vlan_list_expanded = vlan_list_full(vlan_list)
                            valid_vlan = True
                            for vlan in vlan_list_expanded:
                                valid_vlan = validating_ucs.number_in_range('VLAN ID', vlan, 1, 4094)
                                if valid_vlan == False:
                                    break
                            native_count = 0
                            native_vlan = ''
                            if valid_vlan == True:
                                native_vlan = input('If you want to configure one of the VLANs as a Native VLAN in this list add it here. [press enter to skip]:')
                            if not native_vlan == '' and valid_vlan == True:
                                for vlan in vlan_list_expanded:
                                    if int(native_vlan) == int(vlan):
                                        native_count = 1
                                if native_count == 1:
                                    valid = True
                                else:
                                    print(f'\n---------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The Native VLAN was not in the Allowed List.')
                                    print(f'\n---------------------------------------------------------------------------------------\n')

                            elif valid_vlan == True:
                                valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  The allowed vlan list can be in the format of:')
                            print(f'     5 - Single VLAN')
                            print(f'     1-10 - Range of VLANs')
                            print(f'     1,2,3,4,5,11,12,13,14,15 - List of VLANs')
                            print(f'     1-10,20-30 - Ranges and Lists of VLANs')
                            print(f'\n---------------------------------------------------------------------------------------\n')


                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}.  Enter "Y" or "N" [N]? ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # VSAN Policy Module
    #========================================
    def vsan_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vsans'
        org = self.org
        policy_names = []
        policy_type = 'VSAN Policy'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'vsan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    templateVars['priority'] = 'auto'
                    templateVars['receive'] = 'Disabled'
                    templateVars['send'] = 'Disabled'

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # WWNN Pools Module
    #========================================
    def wwnn_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'wwnn_pool'
        org = self.org
        policy_names = []
        policy_type = 'WWNN Pool'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'wwnn_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  WWNN Pool Convention Recommendations:')
            print(f'  - Leverage the Cisco UCS OUI of 20:00:00:25:B5 for the WWNN Pool Prefix.')
            print(f'  - Pool Size can be between 1 and 1000 addresses.')
            print(f'  - Refer to "UCS Naming Conventions 0.5.ppsx" in the Repository for further guidance.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the number for the value to select.  [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        begin = input('What is the Beginning WWNN Address to Assign to the Pool?  [20:00:00:25:B5:00:00:00]: ')
                        if begin == '':
                            begin = '20:00:00:25:B5:00:00:00'
                        valid = validating_ucs.wwxn_address('WWNN Pool Address', begin)

                    valid = False
                    while valid == False:
                        pool_size = input('How Many WWNN Addresses should be added to the Pool?  Range is 1-1000 [512]: ')
                        if pool_size == '':
                            pool_size = '512'
                        valid = validating_ucs.number_in_range('Pool Size', pool_size, 1, 1000)

                    begin = begin.upper()
                    beginx = int(begin.replace(':', ''), 16)
                    add_dec = (beginx + int(pool_size))
                    ending = ':'.join(['{}{}'.format(a, b)
                        for a, b
                        in zip(*[iter('{:012x}'.format(add_dec))]*2)])
                    ending = ending.upper()
                    templateVars['wwnn_blocks'] = [{'from':begin, 'to':ending}]

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

    #========================================
    # WWPN Pools Module
    #========================================
    def wwpn_pools(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_names = []
        policy_type = 'WWPN Pool'
        templateVars = {}
        templateVars['header'] = '%s Variables' % (policy_type)
        templateVars['initial_write'] = True
        templateVars['org'] = org
        templateVars['policy_type'] = policy_type
        templateVars['template_file'] = 'template_open.jinja2'
        templateVars['template_type'] = 'wwpn_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars['initial_write'] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  WWPN Pool Convention Recommendations:')
            print(f'  - Leverage the Cisco UCS OUI of 20:00:00:25:B5 for the WWPN Pool Prefix.')
            print(f'  - For WWPN Pools; create a pool for each Fabric.')
            print(f'  - Pool Size can be between 1 and 1000 addresses.')
            print(f'  - Refer to "UCS Naming Conventions 0.5.ppsx" in the Repository for further guidance.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 1
                policy_loop = False
                while policy_loop == False:

                    name = naming_rule_fabric(loop_count, name_prefix, org)

                    templateVars['name'] = policy_name(name, policy_type)
                    templateVars['descr'] = policy_descr(templateVars['name'], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f"  Assignment order decides the order in which the next identifier is allocated.")
                    print(f"    1. default - (Intersight Default) Assignment order is decided by the system.")
                    print(f"    2. sequential - (Recommended) Identifiers are assigned in a sequential order.")
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['assignment_order'] = input('Specify the number for the value to select.  [2]: ')
                        if templateVars['assignment_order'] == '' or templateVars['assignment_order'] == '2':
                            templateVars['assignment_order'] = 'sequential'
                            valid = True
                        elif templateVars['assignment_order'] == '1':
                            templateVars['assignment_order'] = 'default'
                            valid = True
                        else:
                            print(f'\n---------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n---------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        if loop_count % 2 == 0:
                            begin = input('What is the Beginning WWPN Address to Assign to the Pool?  [20:00:00:25:B5:0B:00:00]: ')
                        else:
                            begin = input('What is the Beginning WWPN Address to Assign to the Pool?  [20:00:00:25:B5:0A:00:00]: ')
                        if begin == '':
                            if loop_count % 2 == 0:
                                begin = '20:00:00:25:B5:0B:00:00'
                            else:
                                begin = '20:00:00:25:B5:0A:00:00'
                        valid = validating_ucs.wwxn_address('WWPN Pool Address', begin)

                    valid = False
                    while valid == False:
                        pool_size = input('How Many WWPN Addresses should be added to the Pool?  Range is 1-1000 [512]: ')
                        if pool_size == '':
                            pool_size = '512'
                        valid = validating_ucs.number_in_range('Pool Size', pool_size, 1, 1000)

                    begin = begin.upper()
                    beginx = int(begin.replace(':', ''), 16)
                    add_dec = (beginx + int(pool_size))
                    ending = ':'.join(['{}{}'.format(a, b)
                        for a, b
                        in zip(*[iter('{:012x}'.format(add_dec))]*2)])
                    ending = ending.upper()
                    templateVars['wwpn_blocks'] = [{'from':begin, 'to':ending}]

                    # Write Policies to Template File
                    templateVars['template_file'] = '%s.jinja2' % (templateVars['template_type'])
                    write_to_template(self, **templateVars)

                    # Add Template Name to Policies Output
                    policy_names.append(templateVars['name'])

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
                    if exit_answer == 'N':
                        policy_loop = True
                        configure_loop = True
                    loop_count += 1
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n---------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n---------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars['template_file'] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

        return policy_names

def naming_rule(name_prefix, name_suffix, org):
    if not name_prefix == '':
        name = '%s_%s' % (name_prefix, name_suffix)
    else:
        name = '%s_%s' % (org, name_suffix)
    return name

def naming_rule_fabric(loop_count, name_prefix, org):
    if loop_count % 2 == 0:
        if not name_prefix == '':
            name = '%s_B' % (name_prefix)
        elif not org == 'default':
            name = '%s_B' % (org)
        else:
            name = 'Fabric_B'
    else:
        if not name_prefix == '':
            name = '%s_A' % (name_prefix)
        elif not org == 'default':
            name = '%s_A' % (org)
        else:
            name = 'Fabric_A'
    return name

def policies_list(policies_list, **templateVars):
    valid = False
    while valid == False:
        print(f"\n---------------------------------------------------------------------------------------\n")
        print(f"  {templateVars['policy']} Options:")
        for i, v in enumerate(policies_list):
            i += 1
            if i < 10:
                print(f'     {i}. {v}')
            else:
                print(f'    {i}. {v}')
        print(f"     99. Do not assign a(n) {templateVars['policy']}.")
        print(f"\n---------------------------------------------------------------------------------------\n")
        policy_temp = input(f"Enter the Index for the {templateVars['policy']} to Assign to {templateVars['name']}: ")
        for i, v in enumerate(policies_list):
            i += 1
            if int(policy_temp) == i:
                policy = v
                valid = True
                return policy
            elif int(policy_temp) == 99:
                policy = ''
                valid = True
                return policy

        if int(policy_temp) == 99:
            policy = ''
            valid = True
            return policy
        elif valid == False:
            print(f"\n---------------------------------------------------------------------------------------\n")
            print(f"  Error!! Invalid Selection.  Please Select a valid Index from the List.")
            print(f"\n---------------------------------------------------------------------------------------\n")

def policy_loop_standard(self, header, initial_policy, template_type):
    # Set the org_count to 0 for the First Organization
    org_count = 0

    # Loop through the orgs discovered by the Class
    for org in self.orgs:

        # Pull in Variables from Class
        templateVars = self.templateVars
        templateVars['org'] = org

        # Define the Template Source
        templateVars['header'] = header
        templateVars['template_type'] = template_type
        template_file = "template_open.jinja2"
        template = self.templateEnv.get_template(template_file)


        # Process the template
        dest_dir = '%s' % (self.type)
        dest_file = '%s.auto.tfvars' % (template_type)
        if initial_policy == True:
            write_method = 'w'
        else:
            write_method = 'a'
        process_method(write_method, dest_dir, dest_file, template, **templateVars)

        # Define the Template Source
        template_file = '%s.jinja2' % (template_type)
        template = self.templateEnv.get_template(template_file)

        if template_type in self.json_data['config']['orgs'][org_count]:
            for item in self.json_data['config']['orgs'][org_count][template_type]:
                # Reset TemplateVars to Default for each Loop
                templateVars = {}
                templateVars['org'] = org

                # Define the Template Source
                templateVars['header'] = header

                # Loop Through Json Items to Create templateVars Blocks
                for k, v in item.items():
                    templateVars[k] = v

                # if template_type == 'iscsi_boot_policies':
                #     print(templateVars)
                # Process the template
                dest_dir = '%s' % (self.type)
                dest_file = '%s.auto.tfvars' % (template_type)
                process_method('a', dest_dir, dest_file, template, **templateVars)

        # Define the Template Source
        template_file = "template_close.jinja2"
        template = self.templateEnv.get_template(template_file)

        # Process the template
        dest_dir = '%s' % (self.type)
        dest_file = '%s.auto.tfvars' % (template_type)
        process_method('a', dest_dir, dest_file, template, **templateVars)

        # Increment the org_count for the next Organization Loop
        org_count += 1

def policy_descr(name, policy_type):
    valid = False
    while valid == False:
        descr = input(f'What is the Description for the {policy_type}?  [{name} {policy_type}]: ')
        if descr == '':
            descr = '%s %s' % (name, policy_type)
        valid = validating_ucs.description(f"{policy_type} Description", descr, 1, 62)
        if valid == True:
            return descr

def policy_name(namex, policy_type):
    valid = False
    while valid == False:
        name = input(f'What is the Name for the {policy_type}?  [{namex}]: ')
        if name == '':
            name = '%s' % (namex)
        valid = validating_ucs.name_rule(f"{policy_type} Name", name, 1, 62)
        if valid == True:
            return name

def policy_template(self, **templateVars):
    policy_names = []
    configure_loop = False
    while configure_loop == False:
        configure = input(f'Do You Want to Configure a(n) {templateVars["policy_type"]}?  Enter "Y" or "N" [Y]: ')
        if configure == 'Y' or configure == '':
            policy_loop = False
            while policy_loop == False:

                valid = False
                while valid == False:
                    policy_file = 'ucs_templates/variables/%s' % (templateVars['policy_file'])
                    if os.path.isfile(policy_file):
                        template_file = open(policy_file, 'r')
                        template_file.seek(0)
                        policy_templates = []
                        for line in template_file:
                            line = line.strip()
                            policy_templates.append(line)
                        print(f"\n---------------------------------------------------------------------------------------\n")
                        print(f"  {templateVars['policy_type']} Templates:")
                        for i, v in enumerate(policy_templates):
                            i += 1
                            if i < 10:
                                print(f'     {i}. {v}')
                            else:
                                print(f'    {i}. {v}')
                        print(f"\n---------------------------------------------------------------------------------------\n")
                    policy_temp = input(f"Enter the Index Number for the {templateVars['policy_type']} Template to Create: ")
                    for i, v in enumerate(policy_templates):
                        i += 1
                        if int(policy_temp) == i:
                            templateVars['policy_template'] = v
                            valid = True
                    if valid == False:
                        print(f"\n---------------------------------------------------------------------------------------\n")
                        print(f"  Error!! Invalid Selection.  Please Select a valid Index from the List.")
                        print(f"\n---------------------------------------------------------------------------------------\n")
                    template_file.close()

                if not templateVars['name_prefix'] == '':
                    name = '%s_%s' % (templateVars['name_prefix'], templateVars['policy_template'])
                else:
                    name = '%s_%s' % (templateVars['org'], templateVars['policy_template'])

                templateVars['name'] = policy_name(name, templateVars['policy_type'])
                templateVars['descr'] = policy_descr(templateVars['name'], templateVars['policy_type'])


                # Add Template Name to Policies Output
                policy_names.append(templateVars['name'])

                # Write Policy to Template
                write_to_template(self, **templateVars)

                exit_answer = input(f'Would You like to Configure another {templateVars["policy_type"]} Template?  Enter "Y" or "N" [N]: ')
                if exit_answer == 'N' or exit_answer == '':
                    policy_loop = True
                    configure_loop = True
        elif configure == 'N':
            configure_loop = True
        else:
            print(f'\n---------------------------------------------------------------------------------------\n')
            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
            print(f'\n---------------------------------------------------------------------------------------\n')

    return policy_names

def policy_variable_list(**templateVars):
    valid = False
    while valid == False:
        policy_file = 'ucs_templates/variables/%s' % (templateVars['policy_file'])
        if os.path.isfile(policy_file):
            var_file = open(policy_file, 'r')
            var_file.seek(0)
            var_options = []
            for line in var_file:
                line = line.strip()
                var_options.append(line)
            print(f"\n---------------------------------------------------------------------------------------\n")
            print(f"  {templateVars['menu_descr']}:")
            for i, v in enumerate(var_options):
                i += 1
                if i < 10:
                    print(f'     {i}. {v}')
                else:
                    print(f'    {i}. {v}')
            print(f"\n---------------------------------------------------------------------------------------\n")
        policy_temp = input(f"{templateVars['input_descr']}: ")
        for i, v in enumerate(var_options):
            i += 1
            if int(policy_temp) == i:
                chosen_value = v
                valid = True
        if valid == False:
            print(f"\n---------------------------------------------------------------------------------------\n")
            print(f"  Error!! Invalid Selection.  Please select a valid option from the List.")
            print(f"\n---------------------------------------------------------------------------------------\n")
        var_file.close()
    return chosen_value

def process_method(wr_method, dest_dir, dest_file, template, **templateVars):
    dest_dir = './UCS/%s/%s' % (templateVars['org'], dest_dir)
    if not os.path.isdir(dest_dir):
        mk_dir = 'mkdir -p %s' % (dest_dir)
        os.system(mk_dir)
    dest_file_path = '%s/%s' % (dest_dir, dest_file)
    if not os.path.isfile(dest_file_path):
        create_file = 'touch %s' % (dest_file_path)
        os.system(create_file)
    tf_file = dest_file_path
    wr_file = open(tf_file, wr_method)

    # Render Payload and Write to File
    payload = template.render(templateVars)
    wr_file.write(payload)
    wr_file.close()

def variable_loop(**templateVars):
    valid = False
    while valid == False:
        print(f'\n---------------------------------------------------------------------------------------')
        print(f'{templateVars["var_description"]}')
        policy_file = 'ucs_templates/variables/%s' % (templateVars['policy_file'])
        if os.path.isfile(policy_file):
            variable_file = open(policy_file, 'r')
            varsx = []
            for line in variable_file:
                varsx.append(line.strip())
            for index, value in enumerate(varsx):
                index += 1
                if index < 10:
                    print(f'     {index}. {value}')
                else:
                    print(f'    {index}. {value}')
        print(f'---------------------------------------------------------------------------------------\n')
        var_selection = input(f'Please Enter the Option Number to Select for {templateVars["var_type"]}: ')
        for index, value in enumerate(varsx):
            index += 1
            if int(var_selection) == index:
                selection = value
                valid = True
        if valid == False:
            print(f'\n---------------------------------------------------------------------------------------\n')
            print(f'  Error!! Invalid Selection.  Please Select a valid Option from the List.')
            print(f'\n---------------------------------------------------------------------------------------\n')
    return selection

def vlan_list_full(vlan_list):
    full_vlan_list = []
    if re.search(r',', str(vlan_list)):
        vlist = vlan_list.split(',')
        for v in vlist:
            if re.fullmatch('^\\d{1,4}\\-\\d{1,4}$', v):
                a,b = v.split('-')
                a = int(a)
                b = int(b)
                vrange = range(a,b+1)
                for vl in vrange:
                    full_vlan_list.append(vl)
            elif re.fullmatch('^\\d{1,4}$', v):
                full_vlan_list.append(v)
    elif re.search('\\-', str(vlan_list)):
        a,b = vlan_list.split('-')
        a = int(a)
        b = int(b)
        vrange = range(a,b+1)
        for v in vrange:
            full_vlan_list.append(v)
    else:
        full_vlan_list.append(vlan_list)
    return full_vlan_list

def write_to_template(self, **templateVars):
    # Define the Template Source
    template = self.templateEnv.get_template(templateVars['template_file'])

    # Process the template
    dest_dir = '%s' % (self.type)
    dest_file = '%s.auto.tfvars' % (templateVars['template_type'])
    if templateVars['initial_write'] == True:
        write_method = 'w'
    else:
        write_method = 'a'
    process_method(write_method, dest_dir, dest_file, template, **templateVars)
