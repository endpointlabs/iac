#!/usr/bin/env python3

import copy
import getpass
import ipaddress
import jinja2
import json
import os, re, sys
import pkg_resources
import subprocess
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
        for item in json_data["config"]["orgs"]:
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
            templateVars["org"] = org

            # Define the Template Source
            templateVars["header"] = header
            templateVars["template_type"] = template_type
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

            if template_type in self.json_data["config"]["orgs"][org_count]:
                for item in self.json_data["config"]["orgs"][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars["org"] = org

                    # Define the Template Source
                    templateVars["header"] = header

                    for k, v in item.items():
                        if (k == 'name' or k == 'descr' or k == 'tags'):
                            templateVars[k] = v

                    templateVars["bios_settings"] = {}
                    for k, v in item.items():
                        if not (k == 'name' or k == 'descr' or k == 'tags'):
                            templateVars["bios_settings"][k] = v

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
            templateVars["org"] = org

            # Define the Template Source
            templateVars["header"] = header
            templateVars["template_type"] = template_type
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

            if template_type in self.json_data["config"]["orgs"][org_count]:
                for item in self.json_data["config"]["orgs"][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars["org"] = org

                    # Define the Template Source
                    templateVars["header"] = header

                    for k, v in item.items():
                        templateVars[k] = v

                    if 'ipv6_blocks' in templateVars:
                        index_count = 0
                        for i in templateVars["ipv6_blocks"]:
                             index_count += 1

                        for r in range(0,index_count):
                            if 'to' in templateVars["ipv6_blocks"][r]:
                                templateVars["ipv6_blocks"][r]["size"] = templateVars["ipv6_blocks"][r].pop('to')
                                templateVars["ipv6_blocks"][r]["size"] = int(
                                    ipaddress.IPv6Address(templateVars["ipv6_blocks"][r]["size"])
                                    ) - int(ipaddress.IPv6Address(templateVars["ipv6_blocks"][r]["from"])) + 1

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
            templateVars["org"] = org

            # Define the Template Source
            templateVars["header"] = header
            templateVars["template_type"] = template_type
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

            if template_type in self.json_data["config"]["orgs"][org_count]:
                for item in self.json_data["config"]["orgs"][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars["org"] = org

                    # Define the Template Source
                    templateVars["header"] = header

                    for k, v in item.items():
                        templateVars[k] = v

                    if 'iqn_blocks' in templateVars:
                        index_count = 0
                        for i in templateVars["iqn_blocks"]:
                             index_count += 1

                        for r in range(0,index_count):
                            if 'to' in templateVars["iqn_blocks"][r]:
                                templateVars["iqn_blocks"][r]["size"] = templateVars["iqn_blocks"][r].pop('to')
                                templateVars["iqn_blocks"][r]["size"] = int(
                                    templateVars["iqn_blocks"][r]["size"]
                                    ) - int(templateVars["iqn_blocks"][r]["from"]) + 1

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
            templateVars["org"] = org

            # Define the Template Source
            templateVars["header"] = header
            templateVars["template_type"] = template_type
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

            if template_type in self.json_data["config"]["orgs"][org_count]:
                for item in self.json_data["config"]["orgs"][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars["org"] = org

                    # Define the Template Source
                    templateVars["header"] = header
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
                            templateVars["port_modes"] = {'port_list': [begin, end], 'slot_id': slot_id}
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
                        templateVars["port_channel_appliances"] = templateVars["appliance_port_channels"]
                        del templateVars["appliance_port_channels"]
                    if 'lan_port_channels' in templateVars:
                        templateVars["port_channel_ethernet_uplinks"] = templateVars["lan_port_channels"]
                        del templateVars["lan_port_channels"]
                    if 'san_port_channels' in templateVars:
                        templateVars["port_channel_fc_uplinks"] = templateVars["san_port_channels"]
                        del templateVars["san_port_channels"]
                        print(templateVars["port_channel_fc_uplinks"])
                    if 'fcoe_port_channels' in templateVars:
                        templateVars["port_channel_fcoe_uplinks"] = templateVars["fcoe_port_channels"]
                        del templateVars["fcoe_port_channels"]
                    if 'appliance_ports' in templateVars:
                        templateVars["port_role_appliances"] = templateVars["appliance_ports"]
                        del templateVars["appliance_ports"]
                    if 'lan_uplink_ports' in templateVars:
                        templateVars["port_role_ethernet_uplinks"] = templateVars["lan_uplink_ports"]
                        del templateVars["lan_uplink_ports"]
                    if 'san_uplink_ports' in templateVars:
                        templateVars["port_role_fc_uplinks"] = templateVars["san_uplink_ports"]
                        del templateVars["san_uplink_ports"]
                    if 'fcoe_uplink_ports' in templateVars:
                        templateVars["port_role_fcoe_uplinks"] = templateVars["fcoe_uplink_ports"]
                        del templateVars["fcoe_uplink_ports"]
                    if 'server_ports' in templateVars:
                        templateVars["port_role_servers"] = templateVars["server_ports"]
                        del templateVars["server_ports"]

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
            templateVars["org"] = org

            # Define the Template Source
            templateVars["header"] = header
            templateVars["template_type"] = template_type
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

            if template_type in self.json_data["config"]["orgs"][org_count]:
                for item in self.json_data["config"]["orgs"][org_count][template_type]:
                    # Reset TemplateVars to Default for each Loop
                    templateVars = {}
                    templateVars["org"] = org

                    # Define the Template Source
                    templateVars["header"] = header

                    for k, v in item.items():
                        if (k == 'name' or k == 'descr' or k == 'tags'):
                            templateVars[k] = v

                templateVars["classes"] = []
                for r in range(0,6):
                    xdict = {}
                    templateVars["classes"].append(xdict)

                class_count = 0
                for item in self.json_data["config"]["orgs"][org_count][template_type][0]["classes"]:
                    for k, v in item.items():
                        templateVars["classes"][class_count][k] = v

                    class_count += 1

                total_weight = 0

                for r in range(0,6):
                    if templateVars["classes"][r]["state"] == 'Enabled':
                        total_weight += int(templateVars["classes"][r]["weight"])

                for r in range(0,6):
                    if templateVars["classes"][r]["state"] == 'Enabled':
                        x = ((int(templateVars["classes"][r]["weight"]) / total_weight) * 100)
                        templateVars["classes"][r]["bandwidth_percent"] = str(x).split('.')[0]
                    else:
                        templateVars["classes"][r]["bandwidth_percent"] = 0

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
        policy_type = 'BIOS Policy'
        policy_x = 'BIOS'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["name_prefix"] = name_prefix
        templateVars["org"] = org
        templateVars["policy_file"] = 'bios_templates.txt'
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'bios_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'  {policy_x} Policies:  To simplify your work, this wizard will use {policy_x}')
        print(f'  Templates that are pre-configured.  You can add custom {policy_x} policy')
        print(f'  configuration to the {templateVars["template_type"]}.auto.tfvars file at your descretion.')
        print(f'  That will not be covered by this wizard as the focus of the wizard is on simplicity.\n')
        print(f'  This wizard will save the configuraton for this section to the following file:')
        print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
        print(f'\n-------------------------------------------------------------------------------------------\n')

        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
        policy_names = policy_template(self, **templateVars)

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Boot Order Policy Module
    #========================================
    def boot_order_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'boot_order'
        org = self.org
        policy_type = 'Boot Order Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'boot_order_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the Index for the value to select [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Ethernet Adapter Policy Module
    #========================================
    def ethernet_adapter_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'Ethernet Adapter Policy'
        policy_x = 'Ethernet Adapter'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["name_prefix"] = name_prefix
        templateVars["org"] = org
        templateVars["policy_file"] = 'ethernet_adapter_templates.txt'
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ethernet_adapter_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'  {policy_x} Policies:  To simplify your work, this wizard will use {policy_x}')
        print(f'  Templates that are pre-configured.  You can add custom {policy_x} policy')
        print(f'  configuration to the {templateVars["template_type"]}.auto.tfvars file at your descretion.')
        print(f'  That will not be covered by this wizard as the focus of the wizard is on simplicity.\n')
        print(f'  This wizard will save the configuraton for this section to the following file:')
        print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
        print(f'\n-------------------------------------------------------------------------------------------\n')

        templateVars["template_file"] = 'ethernet_adapter_templates.jinja2'
        policy_names = policy_template(self, **templateVars)

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Ethernet Network Control Policy Module
    #========================================
    def ethernet_network_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'netwk_ctrl'
        org = self.org
        policy_type = 'Ethernet Network Control Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ethernet_network_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} will allow you to control Network Discovery with ')
            print(f'  protocols like CDP and LLDP as well as MAC Address Control Features.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["action_on_uplink_fail"] = 'linkDown'

                valid = False
                while valid == False:
                    cdp = input('Do you want to enable CDP (Cisco Discovery Protocol) for this Policy?  Enter "Y" or "N" [Y]: ')
                    if cdp == '' or cdp == 'Y':
                        templateVars["cdp_enable"] = True
                        valid = True
                    elif cdp == 'N':
                        templateVars["cdp_enable"] = False
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Option.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    cdp = input('Do you want to enable LLDP (Link Level Discovery Protocol) for this Policy?  Enter "Y" or "N" [Y]: ')
                    if cdp == '' or cdp == 'Y':
                        templateVars["lldp_receive_enable"] = True
                        templateVars["lldp_transmit_enable"] = True
                        valid = True
                    elif cdp == 'N':
                        templateVars["lldp_receive_enable"] = False
                        templateVars["lldp_transmit_enable"] = False
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Option.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'mac_register_mode.txt'
                templateVars["var_description"] = '   MAC Registration Mode:  Default is "nativeVlanOnly".\n   Determines the MAC addresses that have to be registered with the switch.'
                templateVars["var_type"] = 'MAC Registration Mode'
                templateVars["mac_register_mode"] = variable_loop(**templateVars)

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'mac_security_forge.txt'
                templateVars["var_description"] = '   MAC Security Forge:  Default is "allow".\n   Determines if the MAC forging is allowed or denied on an interface.'
                templateVars["var_type"] = 'MAC Security Forge'
                templateVars["mac_security_forge"] = variable_loop(**templateVars)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    action_on_uplink_fail = "{templateVars["action_on_uplink_fail"]}"')
                print(f'    cdp_enable            = {templateVars["cdp_enable"]}')
                print(f'    description           = "{templateVars["descr"]}"')
                print(f'    lldp_enable_receive   = {templateVars["lldp_receive_enable"]}')
                print(f'    lldp_enable_transmit  = {templateVars["lldp_transmit_enable"]}')
                print(f'    mac_register_mode     = "{templateVars["mac_register_mode"]}"')
                print(f'    mac_security_forge    = "{templateVars["mac_security_forge"]}"')
                print(f'    name                  = "{templateVars["name"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Ethernet Network Group Policy Module
    #========================================
    def ethernet_network_group_policies(self):
        name_prefix = self.name_prefix
        name_suffix = ['Management', 'Migration', 'Storage', 'VMs']
        org = self.org
        policy_type = 'Ethernet Network Group Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ethernet_network_group_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} will define the Allowed VLANs on a Server vNIC Template.')
            print(f'  As a recommendation you will need an {policy_type} per vNIC Grouping.')
            print(f'  For Instance with a Virtual Host that may have the following vNIC Pairs:')
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
            print(f'  If you want to Assign a Native VLAN Make sure it is in the allowed list.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            loop_count = 0
            policy_loop = False
            while policy_loop == False:

                name = ''
                for i, v in enumerate(name_suffix):
                    if int(loop_count) == i:
                        if not name_prefix == '':
                            name = '%s_%s' % (name_prefix, v)
                        else:
                            name = '%s_%s' % (org, v)
                if name == '':
                    name = '%s_%s' % (org, 'vlan_group')

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["action_on_uplink_fail"] = 'linkDown'

                valid = False
                while valid == False:
                    ng_vlan_list = input('Enter the VLAN or List of VLANs to add to this VLAN Group: ')
                    if not ng_vlan_list == '':
                        policy_list = [
                            'policies_vlans.vlan_policies.vlan_policy',
                        ]
                        templateVars["allow_opt_out"] = False
                        for policy in policy_list:
                            vlan_policy,policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        vlan_list = []
                        for item in policyData['vlan_policies']:
                            for key, value in item.items():
                                if key == vlan_policy:
                                    for i in value[0]['vlans']:
                                        for k, v in i.items():
                                            for x in v:
                                                for y, val in x.items():
                                                    if y == 'vlan_list':
                                                        vlan_list.append(val)

                        vlan_list = ','.join(vlan_list)
                        vlan_list = vlan_list_full(vlan_list)
                        vlan_list_expanded = vlan_list_full(ng_vlan_list)
                        valid_vlan = True
                        vlans_not_in_domain_policy = []
                        for vlan in vlan_list_expanded:
                            valid_vlan = validating_ucs.number_in_range('VLAN ID', vlan, 1, 4094)
                            if valid_vlan == False:
                                break
                            else:
                                vlan_count = 0
                                for vlans in vlan_list:
                                    if int(vlan) == int(vlans):
                                        vlan_count += 1
                                        break
                                if vlan_count == 0:
                                    vlans_not_in_domain_policy.append(vlans)


                        if len(vlans_not_in_domain_policy) > 0:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error with VLAN(s) assignment!!  The following VLAN(s) are missing.')
                            print(f'  - Domain VLAN Policy: "{vlan_policy}"')
                            print(f'  - Missing VLANs: {vlans_not_in_domain_policy}')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            valid_vlan = False

                        native_count = 0
                        native_vlan = ''
                        if valid_vlan == True:
                            native_valid = False
                            while native_valid == False:
                                native_vlan = input('Do you want to Configure one of the VLANs as a Native VLAN?  [press enter to skip]:')
                                if native_vlan == '':
                                    native_valid = True
                                    valid = True
                                else:
                                    for vlan in vlan_list_expanded:
                                        if int(native_vlan) == int(vlan):
                                            native_count = 1
                                    if not native_count == 1:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! The Native VLAN was not in the Allowed List.')
                                        print(f'  Allowed VLAN List is: "{vlan_list}"')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                    else:
                                        native_valid = True
                                        valid = True

                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  The allowed vlan list can be in the format of:')
                        print(f'     5 - Single VLAN')
                        print(f'     1-10 - Range of VLANs')
                        print(f'     1,2,3,4,5,11,12,13,14,15 - List of VLANs')
                        print(f'     1-10,20-30 - Ranges and Lists of VLANs')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                templateVars["allowed_vlans"] = ng_vlan_list
                if not native_vlan == '':
                    templateVars["native_vlan"] = native_vlan
                else:
                    templateVars["native_vlan"] = ''
                    templateVars.pop('native_vlan')

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    allowed_vlans = "{templateVars["allowed_vlans"]}"')
                print(f'    description   = "{templateVars["descr"]}"')
                print(f'    name          = "{templateVars["name"]}"')
                if not native_vlan == '':
                    print(f'    native_vlan   = {templateVars["native_vlan"]}')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        valid_exit = False
                        while valid_exit == False:
                            if loop_count < 3:
                                exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
                            else:
                                exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                            if (loop_count < 3 and exit_answer == '') or exit_answer == 'Y':
                                loop_count += 1
                                valid_exit = True
                            elif (loop_count > 2 and exit_answer == '') or exit_answer == 'N':
                                policy_loop = True
                                configure_loop = True
                                valid_exit = True
                            else:
                                print(f'\n------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {policy_type} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Ethernet Network Policy Module
    #========================================
    def ethernet_network_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'netwk'
        org = self.org
        policy_type = 'Ethernet Network Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ethernet_network_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the Index for the value to select [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Ethernet QoS Policy Module
    #========================================
    def ethernet_qos_policies(self, domain_mtu):
        name_prefix = self.name_prefix
        name_suffix = ['Management', 'Migration', 'Storage', 'VMs']
        org = self.org
        policy_type = 'Ethernet QoS Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ethernet_qos_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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
            print(f'  It would be a good practice to configure different QoS Priorities for Each vNIC Group.')
            print(f'  For Instance a good practice would be something like the following:')
            print(f'     Management - Silver')
            print(f'     Migration/vMotion - Bronze')
            print(f'     Storage - Platinum')
            print(f'     Virtual Machines - Gold.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            loop_count = 0
            policy_loop = False
            while policy_loop == False:

                name = ''
                for i, v in enumerate(name_suffix):
                    if int(loop_count) == i:
                        if not name_prefix == '':
                            name = '%s_%s' % (name_prefix, v)
                        else:
                            name = '%s_%s' % (org, v)
                if name == '':
                    name = '%s_%s' % (org, 'qos')

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["burst"] = 1024
                templateVars["enable_trust_host_cos"] = False
                templateVars["rate_limit"] = 0

                templateVars["mtu"] = domain_mtu

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'qos_priority.txt'
                templateVars["var_description"] = '   Priority - Default is "Best Effort".\n   The Priority Queue to Assign to this QoS Policy:\n'
                templateVars["var_type"] = 'Priority'
                templateVars["priority"] = variable_loop(**templateVars)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'   description = "{templateVars["descr"]}"')
                print(f'   mtu         = "{templateVars["mtu"]}"')
                print(f'   name        = "{templateVars["name"]}"')
                print(f'   priority    = "{templateVars["priority"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        valid_exit = False
                        while valid_exit == False:
                            if loop_count < 3:
                                exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
                            else:
                                exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                            if (loop_count < 3 and exit_answer == '') or exit_answer == 'Y':
                                loop_count += 1
                                valid_exit = True
                            elif (loop_count > 2 and exit_answer == '') or exit_answer == 'N':
                                policy_loop = True
                                configure_loop = True
                                valid_exit = True
                            else:
                                print(f'\n------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {policy_type} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Fibre-Channel Adapter Policy Module
    #========================================
    def fibre_channel_adapter_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'Fibre-Channel Adapter Policy'
        policy_x = 'Fibre-Channel Adapter'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["name_prefix"] = name_prefix
        templateVars["org"] = org
        templateVars["policy_file"] = 'fibre_channel_adapter_templates.txt'
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'fibre_channel_adapter_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  You can Skip this policy if you are not configuring Fibre-Channel.\n')
            print(f'  {policy_x} Policies:  To simplify your work, this wizard will use {policy_x}')
            print(f'  Templates that are pre-configured.  You can add custom {policy_x} policy')
            print(f'  configuration to the {templateVars["template_type"]}.auto.tfvars file at your descretion.  ')
            print(f'  That will not be covered by this wizard as the focus of the wizard is on simplicity.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':

                templateVars["template_file"] = 'ethernet_adapter_templates.jinja2'
                policy_names = policy_template(self, **templateVars)
                configure_loop = True

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Fibre-Channel Network Policy Module
    #========================================
    def fibre_channel_network_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'Fibre-Channel Network Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'fibre_channel_network_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  You can Skip this policy if you are not configuring Fibre-Channel.\n')
            print(f'  Fibre-Channel Network Policies Notes:')
            print(f'  - You will need one Policy per Fabric.  VSAN A and VSAN B.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 0
                policy_loop = False
                while policy_loop == False:

                    name = naming_rule_fabric(loop_count, name_prefix, org)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'target_platform.txt'
                    templateVars["var_description"] = '    The platform for which the server profile is applicable. It can either be:\n'
                    templateVars["var_type"] = 'Target Platform'
                    target_platform = variable_loop(**templateVars)
                    templateVars["target_platform"] = target_platform

                    if templateVars["target_platform"] == 'Standalone':
                        valid = False
                        while valid == False:
                            templateVars["default_vlan"] = input('What is the Default VLAN you want to Assign to this Policy? ')
                            valid = validating_ucs.number_in_range('Default VLAN', templateVars["default_vlan"], 1, 4094)
                    else:
                        templateVars["default_vlan"] = 0

                    valid = False
                    while valid == False:
                        if loop_count % 2 == 0:
                            templateVars["vsan_id"] = input('What VSAN Do you want to Assign to this Policy?  [100]: ')
                        else:
                            templateVars["vsan_id"] = input('What VSAN Do you want to Assign to this Policy?  [200]: ')
                        if templateVars["vsan_id"] == '':
                            if loop_count % 2 == 0:
                                templateVars["vsan_id"] = 100
                            else:
                                templateVars["vsan_id"] = 200
                        vsan_valid = validating_ucs.number_in_range('VSAN ID', templateVars["vsan_id"], 1, 4094)
                        if vsan_valid == True:
                            if target_platform == 'FIAttached':
                                policy_list = [
                                    'policies.vsan_policies.vsan_policy',
                                ]
                                templateVars["allow_opt_out"] = False
                                for policy in policy_list:
                                    vsan_policy,policyData = policy_select_loop(name_prefix, policy, **templateVars)

                                vsan_list = []
                                for item in policyData['vsan_policies']:
                                    for key, value in item.items():
                                        if key == vsan_policy:
                                            for i in value[0]['vlans']:
                                                for k, v in i.items():
                                                    for x in v:
                                                        for y, val in x.items():
                                                            if y == 'vlan_list':
                                                                vsan_list.append(val)

                                vsan_list = ','.join(vsan_list)
                                vsan_list = vlan_list_full(vsan_list)
                                vsan_count = 0
                                for vsan in vsan_list:
                                    if int(templateVars["vsan_id"]) == int(vsan):
                                        vsan_count = 1
                                        break
                                if vsan_count == 0:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error with VSAN!!  The VSAN {templateVars["vsan_id"]} is not in the VSAN Policy')
                                    print(f'  {vsan_policy}.  Options are {vsan_list}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                else:
                                    valid = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    if templateVars["target_platform"] == 'Standalone':
                        print(f'   default_vlan = "{templateVars["default_vlan"]}"')
                    print(f'   description  = "{templateVars["descr"]}"')
                    print(f'   name         = "{templateVars["name"]}"')
                    print(f'   vsan_id      = "{templateVars["vsan_id"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, loop_count, policy_loop = exit_loop_default_yes(loop_count, policy_type)
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {policy_type} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Fibre-Channel QoS Policy Module
    #========================================
    def fibre_channel_qos_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'qos'
        org = self.org
        policy_type = 'Fibre-Channel QoS Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'fibre_channel_qos_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  You can Skip this policy if you are not configuring Fibre-Channel.\n')
            print(f'  It is a good practice to apply a {policy_type} to the vHBAs.  This wizard')
            print(f'  creates the policy with all the default values, so you only need one')
            print(f'  {policy_type}.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["burst"] = 1024
                    templateVars["max_data_field_size"] = 2112
                    templateVars["rate_limit"] = 0

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    burst               = "{templateVars["burst"]}"')
                    print(f'    description         = "{templateVars["descr"]}"')
                    print(f'    max_data_field_size = "{templateVars["max_data_field_size"]}"')
                    print(f'    name                = "{templateVars["name"]}"')
                    print(f'    rate_limit          = "{templateVars["rate_limit"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Firmware - UCS Domain Module
    #========================================
    def firmware_ucs_domain(self):
        templateVars = {}
        templateVars["header"] = 'UCS Domain Profile Variables'
        templateVars["initial_write"] = True
        templateVars["org"] = self.org
        templateVars["policy_type"] = 'UCS Domain Profile'
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ntp_policies'
        valid = False
        while valid == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
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
            print(f'\n-------------------------------------------------------------------------------------------\n')
            ucs_version = input('Enter the Index Number for the Version of Software to Run: ')
            for i, v in enumerate(versions):
                i += 1
                if int(ucs_version) == i:
                    ucs_domain_version = v
                    valid = True
            if valid == False:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                print(f'\n-------------------------------------------------------------------------------------------\n')
            version_file.close()

    #========================================
    # Flow Control Policy Module
    #========================================
    def flow_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'flow_ctrl'
        org = self.org
        policy_type = 'Flow Control Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'flow_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  The Flow Control Policy will enable Priority Flow Control on the Fabric Interconnects.')
            print(f'  We recommend the default parameters so you will only be asked for the name and')
            print(f'  description for the Policy.  You only need one of these policies for Organization')
            print(f'  {org}.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                templateVars["priority"] = 'auto'
                templateVars["receive"] = 'Enabled'
                templateVars["send"] = 'Enabled'

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description = "{templateVars["descr"]}"')
                print(f'    name        = "{templateVars["name"]}"')
                print(f'    priority    = "{templateVars["priority"]}"')
                print(f'    receive     = "{templateVars["receive"]}"')
                print(f'    send        = "{templateVars["send"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # IMC Access Policy Module
    #========================================
    def imc_access_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'imc_access'
        org = self.org
        policy_type = 'IMC Access Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'imc_access_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  You will need to configure an IMC Access Policy in order to Assign the VLAN and IPs to ')
            print(f'  the Servers for KVM Access.  At this time only inband access is supported in IMM mode.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            loop_count = 0
            policy_loop = False
            while policy_loop == False:
                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["default_vlan"] = 0

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'target_platform.txt'
                templateVars["var_description"] = '    The platform for which the server profile is applicable. It can either be:\n'
                templateVars["var_type"] = 'Target Platform'
                target_platform = variable_loop(**templateVars)
                templateVars["target_platform"] = target_platform

                policy_list = [
                    'pools.ip_pools.inband_ip_pool'
                ]
                templateVars["allow_opt_out"] = False
                for policy in policy_list:
                    templateVars["inband_ip_pool"],policyData = policy_select_loop(name_prefix, policy, **templateVars)

                valid = False
                while valid == False:
                    templateVars["inband_vlan_id"] = input('What VLAN Do you want to Assign to this Policy? ')
                    valid_vlan = validating_ucs.number_in_range('VLAN ID', templateVars["inband_vlan_id"], 1, 4094)
                    if valid_vlan == True:
                        if target_platform == 'FIAttached':
                            policy_list = [
                                'policies_vlans.vlan_policies.vlan_policy',
                            ]
                            templateVars["allow_opt_out"] = False
                            for policy in policy_list:
                                vlan_policy,policyData = policy_select_loop(name_prefix, policy, **templateVars)
                            vlan_list = []
                            for item in policyData['vlan_policies']:
                                for key, value in item.items():
                                    if key == vlan_policy:
                                        for i in value[0]['vlans']:
                                            for k, v in i.items():
                                                for x in v:
                                                    for y, val in x.items():
                                                        if y == 'vlan_list':
                                                            vlan_list.append(val)

                            vlan_list = ','.join(vlan_list)
                            vlan_list = vlan_list_full(vlan_list)
                            vlan_count = 0
                            for vlan in vlan_list:
                                if int(templateVars["inband_vlan_id"]) == int(vlan):
                                    vlan_count = 1
                                    break
                            if vlan_count == 0:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error with Inband VLAN Assignment!!  The VLAN {templateVars["inband_vlan_id"]} is not in the VLAN Policy')
                                print(f'  {vlan_policy}.  VALID VLANs are:{vlan_list}')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                            else:
                                valid = True
                        else:
                            valid = True

                valid = False
                while valid == False:
                    enable_ipv4 = input('Do you want to enable IPv4 for this Policy?  Enter "Y" or "N" [Y]: ')
                    if enable_ipv4 == 'Y' or enable_ipv4 == '':
                        templateVars["ipv4_address_configuration"] = True
                        valid = True
                    else:
                        templateVars["ipv4_address_configuration"] = False
                        valid = True

                valid = False
                while valid == False:
                    enable_ipv4 = input('Do you want to enable IPv6 for this Policy?  Enter "Y" or "N" [N]: ')
                    if enable_ipv4 == 'Y':
                        templateVars["ipv6_address_configuration"] = True
                        valid = True
                    else:
                        templateVars["ipv6_address_configuration"] = False
                        valid = True

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'   description                = "{templateVars["descr"]}"')
                print(f'   inband_ip_pool             = "{templateVars["inband_ip_pool"]}"')
                print(f'   inband_vlan_id             = {templateVars["inband_vlan_id"]}')
                print(f'   ipv4_address_configuration = {templateVars["ipv4_address_configuration"]}')
                print(f'   ipv6_address_configuration = {templateVars["ipv6_address_configuration"]}')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # IP Pools Module
    #========================================
    def ip_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'ip_pool'
        org = self.org
        policy_type = 'IP Pool'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ip_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  At a minimum you will need one IP Pool for KVM Access to Servers.  Currently out-of-band')
            print(f'  management is not supported for KVM access.  This IP Pool will need to be associated to a ')
            print(f'  VLAN assigned to the VLAN Pool of the Domain.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Assignment order decides the order in which the next identifier is allocated.')
                print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid = False
                while valid == False:
                    templateVars["assignment_order"] = input('Specify the number for the value to select.  [2]: ')
                    if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                        templateVars["assignment_order"] = 'sequential'
                        valid = True
                    elif templateVars["assignment_order"] == '1':
                        templateVars["assignment_order"] = 'default'
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    config_ipv4 = input('Do you want to configure IPv4 for this Pool?  Enter "Y" or "N" [Y]: ')
                    if config_ipv4 == 'Y' or config_ipv4 == '':
                        valid = True
                    elif config_ipv4 == 'N':
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

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
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please Verify you have entered the gateway/prefix correctly.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

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
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please Verify the starting IP is in the same network')
                                print(f'  as the Gateway')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

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
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    beginx = int(ipaddress.IPv4Address(starting))
                    add_dec = (beginx + int(pool_size))
                    ending = str(ipaddress.IPv4Address(add_dec))

                    templateVars["ipv4_blocks"] = [{'from':starting, 'to':ending}]
                    templateVars["ipv4_configuration"] = {'gateway':gateway, 'netmask':netmask,
                        'primary_dns':primary_dns, 'secondary_dns':secondary_dns}

                valid = False
                while valid == False:
                    config_ipv6 = input('Do you want to configure IPv6 for this Pool?  Enter "Y" or "N" [Y]: ')
                    if config_ipv6 == 'Y' or config_ipv6 == '':
                        valid = True
                    elif config_ipv6 == 'N':
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                if config_ipv6 == 'Y' or config_ipv6 == '':
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
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please Verify you have entered the gateway/prefix correctly.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

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
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please Verify the starting IP is in the same network')
                                print(f'  as the Gateway')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

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
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    # beginx = int(ipaddress.IPv6Address(starting))
                    # add_dec = (beginx + int(pool_size))
                    # ending = str(ipaddress.IPv6Address(add_dec))

                    templateVars["ipv6_blocks"] = [{'from':starting, 'size':pool_size}]
                    templateVars["ipv6_configuration"] = {'gateway':gateway, 'prefix':prefix,
                        'primary_dns':primary_dns, 'secondary_dns':secondary_dns}

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    assignment_order = "{templateVars["assignment_order"]}"')
                print(f'    description      = "{templateVars["descr"]}"')
                print(f'    name             = "{templateVars["name"]}"')
                if config_ipv4 == 'Y' or config_ipv4 == '':
                    print(f'    ipv4_blocks = [')
                    for item in templateVars["ipv4_blocks"]:
                        print('      {')
                        for k, v in item.items():
                            if k == 'from':
                                print(f'        from = "{v}" ')
                            elif k == 'to':
                                print(f'        to   = "{v}"')
                        print('      }')
                    print(f'    ]')
                    print('    ipv4_configuration = {')
                    print('      {')
                    for k, v in templateVars["ipv4_configuration"].items():
                        if k == 'gateway':
                            print(f'        gateway       = "{v}"')
                        elif k == 'netmask':
                            print(f'        netmask       = "{v}"')
                        elif k == 'primary_dns':
                            print(f'        primary_dns   = "{v}"')
                        elif k == 'secondary_dns':
                            print(f'        secondary_dns = "{v}"')
                    print('      }')
                    print('    }')
                if config_ipv6 == 'Y' or config_ipv6 == '':
                    print(f'    ipv6_blocks = [')
                    for item in templateVars["ipv6_blocks"]:
                        print('      {')
                        for k, v in item.items():
                            if k == 'from':
                                print(f'        from = {v}')
                            elif k == 'size':
                                print(f'        size = {v}')
                        print('      }')
                    print(f'    ]')
                    print('    ipv6_configuration = {')
                    print('      {')
                    for k, v in templateVars["ipv6_configuration"].items():
                        if k == 'gateway':
                            print(f'        gateway       = "{v}"')
                        elif k == 'prefix':
                            print(f'        prefix        = "{v}"')
                        elif k == 'primary_dns':
                            print(f'        primary_dns   = "{v}"')
                        elif k == 'secondary_dns':
                            print(f'        secondary_dns = "{v}"')
                    print('      }')
                    print('    }')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # IPMI over LAN Policy Module
    #========================================
    def ipmi_over_lan_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ipmi'
        org = self.org
        policy_type = 'IPMI over LAN Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ipmi_over_lan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} will configure IPMI over LAN access on a Server Profile.  This policy')
            print(f'  allows you to determine whether IPMI commands can be sent directly to the server, using ')
            print(f'  the IP address.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["enabled"] = True

                    valid = False
                    while valid == False:
                        encrypt_traffic = input('Do you want to encrypt IPMI over LAN Traffic?  Enter "Y" or "N" [Y]: ')
                        if encrypt_traffic == 'Y' or encrypt_traffic == '':
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  The ipmi_key Must be in Hexidecimal Format and no longer than 40 characters.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            valid_password = False
                            while valid_password == False:
                                ipmi_key = getpass.getpass(prompt='Enter ipmi_key: ')
                                valid_password = validating_ucs.ipmi_key_check(ipmi_key)

                            templateVars["ipmi_key"] = 1
                            os.environ['TF_VAR_ipmi_key_1'] = '%s' % (ipmi_key)
                            valid = True
                        else:
                            valid = True

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'ipmi_privileges.txt'
                    templateVars["var_description"] = '   Privilege - The highest privilege level that can be assigned to an IPMI session on a server.'
                    templateVars["var_type"] = 'Privilege'
                    templateVars["privilege"] = variable_loop(**templateVars)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'   description = "{templateVars["descr"]}"')
                    print(f'   enabled     = {templateVars["enabled"]}')
                    if templateVars["ipmi_key"]:
                        print(f'   ipmi_key    = "Sensitive_value"')
                    print(f'   name        = "{templateVars["name"]}"')
                    print(f'   privilege   = "{templateVars["privilege"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # IQN Pools Module
    #========================================
    def iqn_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'iqn_pool'
        org = self.org
        policy_type = 'IQN Pool'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'iqn_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the Index for the value to select [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  The iSCSI Qualified Name (IQN) format is: iqn.yyyy-mm.naming-authority:unique name, where:')
                    print(f'    - literal iqn (iSCSI Qualified Name) - always iqn')
                    print(f'    - date (yyyy-mm) that the naming authority took ownership of the domain')
                    print(f'    - reversed domain name of the authority (e.g. org.linux, com.example, com.cisco)')
                    print(f'    - unique name is any name you want to use, for example, the name of your host. The naming')
                    print(f'      authority must make sure that any names assigned following the colon are unique, such as:')
                    print(f'        * iqn.1984-12.com.cisco:lnx1')
                    print(f'        * iqn.1984-12.com.cisco:win-server1')
                    print(f'        * iqn.1984-12.com.cisco:win-server1')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars['prefix'] = input(f'\nWhat is the IQN Prefix you would like to assign to the Pool?  [iqn.1984-12.com.cisco]: ')
                        if templateVars['prefix'] == '':
                            templateVars['prefix'] = 'iqn.1984-12.com.cisco'

                        suffix = input(f'\nWhat is the IQN Suffix you would like to assign to the Pool?  [ucs-host]: ')
                        if suffix == '':
                            suffix = 'ucs-host'

                        pool_from = input(f'\nWhat is the first Suffix Number in the Block?  [1]: ')
                        if pool_from == '':
                            pool_from = '1'
                        valid_from = validating_ucs.number_in_range('IQN Pool From', pool_from, 1, 1000)

                        pool_size = input(f'\nWhat is the size of the Block?  [512]: ')
                        if pool_size == '':
                            pool_size = '512'
                        valid_size = validating_ucs.number_in_range('IQN Pool Size', pool_size, 1, 1000)

                        from_iqn = '%s:%s%s' % (templateVars['prefix'], suffix, pool_from)
                        valid_iqn = validating_ucs.iqn_address('IQN Staring Address', from_iqn)

                        if valid_from == True and valid_size == True and valid_iqn == True:
                            valid = True
                    templateVars["iqn_blocks"] = [
                        {
                            'from':pool_from,
                            'size':pool_size,
                            'suffix':suffix
                        }
                    ]
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'    assignment_order = "{templateVars["assignment_order"]}"')
                    print(f'    description      = "{templateVars["descr"]}"')
                    print(f'    name             = "{templateVars["name"]}"')
                    print(f'    prefix           = "{templateVars["prefix"]}"')
                    print(f'    iqn_blocks = [')
                    for i in templateVars["iqn_blocks"]:
                        print(f'      ''{')
                        for k, v in i.items():
                            if k == 'from':
                                print(f'        from   = {v}')
                            elif k == 'size':
                                print(f'        size   = {v}')
                            elif k == 'suffix':
                                print(f'        suffix = "{v}"')
                        print(f'      ''}')
                    print(f'    ]')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # iSCSI Adapter Policy Module
    #========================================
    def iscsi_adapter_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'adapter'
        org = self.org
        policy_type = 'iSCSI Adapter Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'iscsi_adapter_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the Index for the value to select [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # iSCSI Boot Policy Module
    #========================================
    def iscsi_boot_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'boot'
        org = self.org
        policy_type = 'iSCSI Boot Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'iscsi_boot_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the Index for the value to select [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # iSCSI Static Target Policy Module
    #========================================
    def iscsi_static_target_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'target'
        org = self.org
        policy_type = 'iSCSI Static Target Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'iscsi_static_target_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["priority"] = 'auto'
                    templateVars["receive"] = 'Disabled'
                    templateVars["send"] = 'Disabled'

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # LAN Connectivity Policy Module
    #========================================
    def lan_connectivity_policies(self, policies):
        name_prefix = self.name_prefix
        name_suffix = 'lan'
        org = self.org
        policy_type = 'LAN Connectivity Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'lan_connectivity_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure vNIC adapters for Server Profiles.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            loop_count = 1
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                valid = False
                while valid == False:
                    azure_stack_qos = input(f'\nNote: Enabling AzureStack-Host QoS on an adapter allows the user to carve out \n'\
                        'traffic classes for RDMA traffic which ensures that a desired portion of the bandwidth is allocated to it.\n\n'\
                        'Do you want to Enable Azure Stack Host QoS for this LAN Policy?    Enter "Y" or "N" [N]: ')
                    if azure_stack_qos == '' or azure_stack_qos == 'N':
                        templateVars["enable_azure_stack_host_qos"] = False
                        valid = True
                    elif azure_stack_qos == 'Y':
                        templateVars["enable_azure_stack_host_qos"] = True
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    question = input(f'\nDo you want to Enable iSCSI Policies for this LAN Connectivity Policy?  Enter "Y" or "N" [N]: ')
                    if question == '' or question == 'N':
                        iscsi_policies = False
                        valid = True
                    elif question == 'Y':
                        iscsi_policies = True
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                if iscsi_policies == True:
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'iqn_allocation_type.txt'
                    templateVars["var_description"] = '    Allocation Type of iSCSI Qualified Name.  Options are:\n'
                    templateVars["var_type"] = 'IQN Allocation Type'
                    templateVars["iqn_allocation_type"] = variable_loop(**templateVars)
                    if templateVars["iqn_allocation_type"] == 'Pool':
                        templateVars["iqn_static_identifier"] = ''

                        policy_list = ['iqn_pools']
                        templateVars["allow_opt_out"] = False
                        for policy in policy_list:
                            templateVars["policies"] = policies.get(policy)
                            templateVars['inband_ip_pool'] = choose_policy(policy, **templateVars)
                    else:
                        templateVars["iqn_pool"] = ''
                        valid = False
                        while valid == False:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  User provided static iSCSI Qualified Name (IQN) for use as initiator identifiers by iSCSI')
                            print(f'  vNICs.')
                            print(f'  The iSCSI Qualified Name (IQN) format is: iqn.yyyy-mm.naming-authority:unique name, where:')
                            print(f'    - literal iqn (iSCSI Qualified Name) - always iqn')
                            print(f'    - date (yyyy-mm) that the naming authority took ownership of the domain')
                            print(f'    - reversed domain name of the authority (e.g. org.linux, com.example, com.cisco)')
                            print(f'    - unique name is any name you want to use, for example, the name of your host. The naming')
                            print(f'      authority must make sure that any names assigned following the colon are unique, such as:')
                            print(f'        * iqn.1984-12.com.cisco:lnx1')
                            print(f'        * iqn.1984-12.com.cisco:win-server1')
                            print(f'        * iqn.1984-12.com.cisco:win-server1')
                            print(f'  Note: You can also obtain an IQN by going to any Linux system and typing in the command:')
                            print(f'        - iscsi-iname')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            question = input(f'\nWould you Like the script to auto generate an IQN For you?  Enter "Y" or "N" [Y]: ')
                            if question == '' or question == 'Y':
                                p = subprocess.Popen(['iscsi-iname'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
                                for line in iter(p.stdout.readline, b''):
                                    line = line.decode("utf-8")
                                    line = line.strip()
                                    suffix = line.split(':')[1]
                                    templateVars["iqn_static_identifier"] = 'iqn.1984-12.com.cisco:%s' % (suffix)
                                valid = True
                            elif question == 'N':
                                templateVars["iqn_static_identifier"] = input(f'What is the Static IQN you would like to assign to this LAN Policy?  ')
                                if not templateVars["iqn_static_identifier"] == '':
                                    valid = validating_ucs.iqn_address('IQN Static Identifier', templateVars["iqn_static_identifier"])

                else:
                    templateVars["iqn_allocation_type"] = 'None'
                    templateVars["iqn_pool"] = ''
                    templateVars["iqn_static_identifier"] = ''

    #========================================
    # LDAP Policy Module
    #========================================
    def ldap_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ldap'
        org = self.org
        policy_type = 'LDAP Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ldap_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} stores and maintains directory information in a network. When LDAP is ')
            print(f'  enabled in the Cisco IMC, user authentication and role authorization is performed by the ')
            print(f'  LDAP server for user accounts not found in the local user database. You can enable and ')
            print(f'  configure LDAP, and configure LDAP servers and LDAP groups.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 1
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["enable_ldap"] = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  The LDAP Base domain that all users must be in.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        domain = input(f'What is your LDAP Base Domain? [example.com]: ')
                        if domain == '':
                            domain = 'example.com'
                        valid = validating_ucs.domain('LDAP Domain', domain)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Base Distinguished Name (DN). Starting point from where the server will search for users')
                    print(f'  and groups. An example would be "dc=example,dc=com".')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        domain_split = domain.split('.')
                        base_dn_var = 'DC=%s' % (',DC='.join(domain_split))

                        base_dn = input(f'What is your Base Distinguished Name?  [{base_dn_var}]: ')
                        if base_dn == '':
                            base_dn = base_dn_var
                        base_split = base_dn.split(',')
                        base_count = 0
                        for x in base_split:
                            if not re.search(r'^(dc)\=[a-zA-Z0-9\-]+$', x, re.IGNORECASE):
                                base_count += 1
                        if base_count == 0:
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! "{base_dn}" is not a valid Base DN.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  LDAP authentication timeout duration, in seconds.  Range is 0 to 180.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        base_timeout = input(f'What do you want set for LDAP Authentication Timeout?  [0]: ')
                        if base_timeout == '':
                            base_timeout = 0
                        if re.fullmatch(r'[0-9]+', str(base_timeout)):
                            minNum = 0
                            maxNum = 180
                            varName = 'LDAP Timeout'
                            varValue = base_timeout
                            valid = validating_ucs.number_in_range(varName, varValue, minNum, maxNum)
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter a number in the range of 0 to 180.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    templateVars["base_settings"] = {
                        'base_dn':base_dn,
                        'domain':domain,
                        'timeout':base_timeout
                    }

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'ldap_bind_method.txt'
                    templateVars["var_description"] = '    Authentication method to access LDAP servers.\n'\
                        '    - Anonymous - Requires no username and password. If this option is selected and the \n'\
                        '        LDAP server is configured for Anonymous logins, then the user gains access.\n'\
                        '    - ConfiguredCredentials - Requires a known set of credentials to be specified for \n'\
                        '        the initial bind process. If the initial bind process succeeds, then the \n'\
                        '        distinguished name (DN) of the user name is queried and re-used for the re-binding  \n'\
                        '        process. If the re-binding process fails, then the user is denied access.\n'\
                        '    - LoginCredentials - (Default) Requires the user credentials. If the bind process \n'\
                        '        fails, then user is denied access.\n'
                    templateVars["var_type"] = 'LDAP Binding Method'
                    bind_method = variable_loop(**templateVars)

                    if not bind_method == 'LoginCredentials':
                        valid = False
                        while valid == False:
                            varUser = input(f'What is the username you want to use for authentication? ')
                            varOU = input(f'What is the Organizational Unit for {varUser}? ')
                            bind_dn = input(f'What is the Distinguished Name for the user? [CN={varUser},OU={varOU},{base_dn}]')
                            if bind_dn == '':
                                bind_dn = 'CN=%s,OU=%s,%s' % (varUser, varOU, base_dn)
                            # regex = re.compile(r'^(cn|ou|dc)\=[a-zA-Z0-9\\\,\+\$ ]+$')
                            # bind_split = bind_dn.split(',')
                            # for x in bind_split:
                            #     reg_test = (regex, bind_dn, re.IGNORECASE)
                            minLength = 1
                            maxLength = 254
                            varName = 'LDAP Bind DN'
                            varValue = bind_dn
                            valid = validating_ucs.string_length(varName, varValue, minLength, maxLength)

                        valid = False
                        while valid == False:
                            secure_passphrase = getpass.getpass(prompt='What is the password of the user for initial bind process? ')
                            minLength = 1
                            maxLength = 254
                            rePattern = '^[\\S]+$'
                            varName = 'LDAP Password'
                            varValue = secure_passphrase
                            valid_passphrase = validating_ucs.length_and_regex_sensitive(rePattern, varName, varValue, minLength, maxLength)
                            if valid_passphrase == True:
                                os.environ['TF_VAR_binding_parameters_password'] = '%s' % (secure_passphrase)
                                valid = True
                        templateVars["binding_parameters"] = {
                            'bind_dn':bind_dn,
                            'bind_method':bind_method
                        }
                    else:
                        templateVars["binding_parameters"] = {
                            'bind_method':bind_method
                        }
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Secure LDAP is not supported but LDAP encryption is.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        enable_encryption = input(f'\nDo you want to encrypt all information sent to the LDAP server?  Enter "Y" or "N" [Y]: ')
                        if enable_encryption == 'N':
                            templateVars["enable_encryption"] = False
                            valid = True
                        elif enable_encryption == '' or enable_encryption == 'Y':
                            templateVars["enable_encryption"] = True
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  If enabled, user authorization is also done at the group level for LDAP users not in the')
                    print(f'  local user database.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        group_auth = input(f'\nDo you want to enable Group Authorization?  Enter "Y" or "N" [Y]: ')
                        if group_auth == 'N':
                            templateVars["enable_group_authorization"] = False
                            valid = True
                        elif group_auth == '' or group_auth == 'Y':
                            templateVars["enable_group_authorization"] = True
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  This Section gives you the option to query DNS for LDAP Server information isntead of')
                    print(f'  defining the LDAP Servers.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        ldap_from_dns = input(f'\nDo you want to use DNS for LDAP Server discovery?  Enter "Y" or "N" [N]: ')
                        if ldap_from_dns == '' or ldap_from_dns == 'N':
                            ldap_from_dns = False
                            valid = True
                        elif ldap_from_dns == 'Y':
                            ldap_from_dns = True
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    if ldap_from_dns == True:
                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'ldap_source.txt'
                        templateVars["var_description"] = '    Specifies how to obtain the domain name used for the \n'\
                            '    DNS SRV request. It can be one of the following:\n'\
                            '    - Configured - specifies using the configured-search domain.\n'\
                            '    - ConfiguredExtracted - specifies using the domain name extracted from the login ID \n'\
                            '        than the configured-search domain.\n'\
                            '    - Extracted - (Default) specifies using domain name extracted-domain from the login ID.\n'
                        templateVars["var_type"] = 'LDAP Domain Source'
                        varSource = variable_loop(**templateVars)

                        if not varSource == 'Extracted':
                            valid = False
                            while valid == False:
                                searchDomain = input(f'\nNote: Domain that acts as a source for a DNS query.\n'\
                                    'What is the Search Domain? ')
                                valid = validating_ucs.domain('Search Domain', searchDomain)

                            valid = False
                            while valid == False:
                                searchForest = input(f'\nNote: Forst that acts as a source for a DNS query.\n'\
                                    'What is the Search Forest? ')
                                valid = validating_ucs.domain('Search Forest', searchForest)
                            templateVars["ldap_From_dns"] = {
                                'enable':True,
                                'search_domain':searchDomain,
                                'search_forest':searchForest,
                                'source':varSource
                            }
                        else:
                            templateVars["ldap_From_dns"] = {
                                'enable':True,
                                'source':varSource
                            }

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  An LDAP attribute that contains the role and locale information for the user. This ')
                    print(f'  property is always a name-value pair. The system queries the user record for the value ')
                    print(f'  that matches this attribute name.')
                    print(f'  The LDAP attribute can use an existing LDAP attribute that is mapped to the Cisco IMC user')
                    print(f'  roles and locales, or can modify the schema such that a new LDAP attribute can be created.')
                    print(f'  For example, CiscoAvPair.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        varAttribute = input(f'What is the attribute to use for the LDAP Search?  [CiscoAvPair]: ')
                        if varAttribute == '':
                            varAttribute = 'CiscoAvPair'
                        valid = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  This field must match the configured attribute in the schema on the LDAP server.')
                    print(f'  By default, this field displays sAMAccountName.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        varFilter = input(f'What is the Filter to use for matching the username?  [sAMAccountName]: ')
                        if varFilter == '':
                            varFilter = 'sAMAccountName'
                        valid = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  This field must match the configured attribute in the schema on the LDAP server.')
                    print(f'  By default, this field displays memberOf.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        varGroupAttribute = input(f'What is the Group Attribute to use for matching the Group Names?  [memberOf]: ')
                        if varGroupAttribute == '':
                            varGroupAttribute = 'memberOf'
                        valid = True

                    templateVars["search_parameters"] = {
                        'attribute':varAttribute,
                        'filter':varFilter,
                        'group_attribute':varGroupAttribute
                    }

                    valid = False
                    while valid == False:
                        varNested = input(f'What is the Search depth to look for a nested LDAP group in an LDAP group map?  Range is 1 to 128.  [128]: ')
                        if varNested == '':
                            varNested = 128
                        if re.fullmatch(r'^[0-9]+', str(varNested)):
                            minNum = 1
                            maxNum = 128
                            varName = 'Nested Group Search Depth'
                            varValue = varNested
                            valid = validating_ucs.number_in_range(varName, varValue, minNum, maxNum)
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter a port in the range of {minNum} and {maxNum}.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    templateVars["nested_group_search_depth"] = varNested
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'ldap_search_precedence.txt'
                    templateVars["var_description"] = '    Search precedence between local user database and LDAP \n'\
                        '    user database.\n'\
                        '    - LocalUserDb - (Default) Precedence is given to local user database while searching.\n'\
                        '    - LDAPUserDb - Precedence is given to LADP user database while searching.\n'
                    templateVars["var_type"] = 'User Search Precedence'
                    templateVars["user_search_precedence"] = variable_loop(**templateVars)

                    templateVars["ldap_groups"] = []
                    inner_loop_count = 1
                    sub_loop = False
                    while sub_loop == False:
                        question = input(f'\nWould you like to configure an LDAP Group?  Enter "Y" or "N" [Y]: ')
                        if question == '' or question == 'Y':
                            valid_sub = False
                            while valid_sub == False:
                                valid = False
                                while valid == False:
                                    varGroup = input(f'What is Group you would like to add from LDAP? ')
                                    if not varGroup == '':
                                        minLength = 1
                                        maxLength = 127
                                        rePattern = '^([^+\\-][a-zA-Z0-9\\=\\!\\#\\$\\%\\(\\)\\+,\\-\\.\\:\\;\\@ \\_\\{\\|\\}\\~\\?\\&]+)$'
                                        varName = 'LDAP Group'
                                        varValue = varGroup
                                        valid = validating_ucs.length_and_regex(rePattern, varName, varValue, minLength, maxLength)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please Re-enter the LDAP Group.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                templateVars["multi_select"] = False
                                templateVars["policy_file"] = 'local_role.txt'
                                templateVars["var_description"] = '    What Role would you like to assign to this LDAP Group?\n'
                                templateVars["var_type"] = 'Group Role'
                                role = variable_loop(**templateVars)

                                ldap_group = {
                                    'group':varGroup,
                                    'role':role
                                }

                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'   group = "{varGroup}"')
                                print(f'   role  = "{role}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = False
                                while valid_confirm == False:
                                    confirm_config = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                                    if confirm_config == 'Y' or confirm_config == '':
                                        templateVars["ldap_groups"].append(ldap_group)
                                        valid_exit = False
                                        while valid_exit == False:
                                            loop_exit = input(f'Would You like to Configure another LDAP Group?  Enter "Y" or "N" [N]: ')
                                            if loop_exit == 'Y':
                                                inner_loop_count += 1
                                                valid_confirm = True
                                                valid_exit = True
                                            elif loop_exit == 'N' or loop_exit == '':
                                                sub_loop = True
                                                valid_confirm = True
                                                valid_exit = True
                                                valid_sub = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                    elif confirm_config == 'N':
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Starting LDAP Group Configuration Over.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                        elif question == 'N':
                            sub_loop = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    templateVars["ldap_servers"] = []
                    inner_loop_count = 1
                    sub_loop = False
                    while sub_loop == False:
                        question = input(f'\nWould you like to configure LDAP Servers?  Enter "Y" or "N" [Y]: ')
                        if question == '' or question == 'Y':
                            valid_sub = False
                            while valid_sub == False:
                                valid = False
                                while valid == False:
                                    varServer = input(f'What is Hostname/IP of the LDAP Server? ')
                                    varName = 'LDAP Server'
                                    varValue = varServer
                                    if re.fullmatch(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$', varServer):
                                        valid = validating_ucs.ip_address(varName, varValue)
                                    else:
                                        valid = validating_ucs.dns_name(varName, varValue)

                                valid = False
                                while valid == False:
                                    if templateVars["enable_encryption"] == True:
                                        xPort = 636
                                    else:
                                        xPort = 389
                                    varPort = input(f'What is Port for {varServer}? [{xPort}]: ')
                                    if varPort == '':
                                        varPort = xPort
                                    if re.fullmatch(r'^[0-9]+', str(varPort)):
                                        minNum = 1
                                        maxNum = 65535
                                        varName = 'Server Port'
                                        varValue = varPort
                                        valid = validating_ucs.number_in_range(varName, varValue, minNum, maxNum)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter a port in the range of {minNum} and {maxNum}.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                ldap_server = {
                                    'port':varPort,
                                    'server':varServer
                                }

                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'   port   = "{varPort}"')
                                print(f'   server = "{varServer}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = False
                                while valid_confirm == False:
                                    confirm_config = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                                    if confirm_config == 'Y' or confirm_config == '':
                                        templateVars["ldap_servers"].append(ldap_server)
                                        valid_exit = False
                                        while valid_exit == False:
                                            loop_exit = input(f'Would You like to Configure another LDAP Server?  Enter "Y" or "N" [N]: ')
                                            if loop_exit == 'Y':
                                                inner_loop_count += 1
                                                valid_confirm = True
                                                valid_exit = True
                                            elif loop_exit == 'N' or loop_exit == '':
                                                sub_loop = True
                                                valid_confirm = True
                                                valid_exit = True
                                                valid_sub = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                    elif confirm_config == 'N':
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Starting LDAP Server Configuration Over.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                        elif question == 'N':
                            sub_loop = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'    base_settings = ''{')
                    print(f'      base_dn = "{templateVars["base_settings"]["base_dn"]}"')
                    print(f'      domain  = "{templateVars["base_settings"]["domain"]}"')
                    print(f'      timeout = "{templateVars["base_settings"]["timeout"]}"')
                    print(f'    ''}')
                    print(f'    binding_parameters = ''{')
                    if not bind_method == 'LoginCredentials':
                        print(f'      bind_dn     = "{templateVars["binding_parameters"]["bind_dn"]}"')
                    print(f'      bind_method = "{templateVars["binding_parameters"]["bind_method"]}"')
                    print(f'    ''}')
                    print(f'    description                = "{templateVars["descr"]}"')
                    print(f'    enable_encryption          = {templateVars["enable_encryption"]}')
                    print(f'    enable_group_authorization = {templateVars["enable_group_authorization"]}')
                    print(f'    enable_ldap                = {templateVars["enable_ldap"]}')
                    if not ldap_from_dns == False:
                        print(f'    ldap_from_dns = ''{')
                        print(f'      enable        = True')
                        if not varSource == 'Extracted':
                            print(f'      search_domain = "{searchDomain}"')
                            print(f'      search_domain = "{searchForest}"')
                        print(f'      source        = "{varSource}"')
                        print(f'    ''}')
                    print(f'    name                      = "{templateVars["name"]}"')
                    print(f'    nested_group_search_depth = "{templateVars["nested_group_search_depth"]}"')
                    if len(templateVars["ldap_groups"]) > 0:
                        print(f'    ldap_groups = ''{')
                        for item in templateVars["ldap_groups"]:
                            for k, v in item.items():
                                if k == 'group':
                                    print(f'      "{v}" = ''{')
                            for k, v in item.items():
                                if k == 'role':
                                    print(f'        {k} = "{v}"')
                            print(f'      ''}')
                        print(f'    ''}')
                    if len(templateVars["ldap_servers"]) > 0:
                        print(f'    ldap_servers = ''{')
                        for item in templateVars["ldap_servers"]:
                            for k, v in item.items():
                                if k == 'server':
                                    print(f'      "{v}" = ''{')
                            for k, v in item.items():
                                if k == 'port':
                                    print(f'        {k} = {v}')
                            print(f'      ''}')
                        print(f'    ''}')
                    print(f'    user_search_precedence = "{templateVars["user_search_precedence"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Link Aggregation Policy Module
    #========================================
    def link_aggregation_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'link_agg'
        org = self.org
        policy_type = 'Link Aggregation Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'link_aggregation_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A Link Aggregation Policy will assign LACP settings to the Ethernet Port-Channels and')
            print(f'  uplinks.  We recommend the default wizard settings so you will only be asked for the ')
            print(f'  name and description for the Policy.  You only need one of these policies for ')
            print(f'  Organization {org}.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                templateVars["lacp_rate"] = 'normal'
                templateVars["suspend_individual"] = False

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description        = "{templateVars["descr"]}"')
                print(f'    lacp_rate          = "{templateVars["lacp_rate"]}"')
                print(f'    name               = "{templateVars["name"]}"')
                print(f'    suspend_individual = {templateVars["suspend_individual"]}')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Link Control Policy Module
    #========================================
    def link_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'link_ctrl'
        org = self.org
        policy_type = 'Link Control Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'link_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A Link Control Policy will configure the Unidirectional Link Detection Protocol for')
            print(f'  Ethernet Uplinks/Port-Channels.')
            print(f'  We recommend the wizards default parameters so you will only be asked for the name')
            print(f'  and description for the Policy.  You only need one of these policies for')
            print(f'  Organization {org}.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                templateVars["admin_state"] = 'Enabled'
                templateVars["mode"] = 'normal'

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    admin_state = "{templateVars["admin_state"]}"')
                print(f'    description = "{templateVars["descr"]}"')
                print(f'    mode        = "{templateVars["mode"]}"')
                print(f'    name        = "{templateVars["name"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Local User Policy Module
    #========================================
    def local_user_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'local_users'
        org = self.org
        policy_type = 'Local User Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'local_user_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure servers with Local Users for KVM Access.  This Policy ')
            print(f'  is not required to standup a server but is a good practice for day 2 support.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 1
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    valid = False
                    while valid == False:
                        always_send = input(f'\nNote: Always Send User Password - If the option is not set to true, user passwords will only \n'\
                            'be sent to endpoint devices for new users and if a user password is changed for existing users.\n\n'\
                            'Do you want Intersight to Always send the user password with policy updates?  Enter "Y" or "N" [N]: ')
                        if always_send == '' or always_send == 'N':
                            templateVars["always_send_user_password"] = False
                            valid = True
                        elif always_send == 'Y':
                            templateVars["always_send_user_password"] = True
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        always_send = input(f'\nEnforce Strong Password, Enables a strong password policy. Strong password requirements:\n'\
                            '  A. The password must have a minimum of 8 and a maximum of 20 characters.\n'\
                            "  B. The password must not contain the User's Name.\n"\
                            '  C. The password must contain characters from three of the following four categories.\n'\
                            '    1. English uppercase characters (A through Z).\n'\
                            '    2. English lowercase characters (a through z).\n'\
                            '    3. Base 10 digits (0 through 9).\n'\
                            '    4. Non-alphabetic characters (! , @, #, $, %, ^, &, *, -, _, +, =)\n\n'\
                            'Do you want to Enforce Strong Passwords?  Enter "Y" or "N" [Y]: ')
                        if always_send == 'N':
                            templateVars["enforce_strong_password"] = False
                            valid = True
                        if always_send == '' or always_send == 'Y':
                            templateVars["enforce_strong_password"] = True
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        always_send = input(f'\nDo you want to Enable password Expiry on the Endpoint?  Enter "Y" or "N" [Y]: ')
                        if always_send == 'N':
                            templateVars["enable_password_expiry"] = False
                            valid = True
                        elif always_send == '' or always_send == 'Y':
                            templateVars["enable_password_expiry"] = True
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    if templateVars["enable_password_expiry"] == True:
                        valid = False
                        while valid == False:
                            templateVars["grace_period"] = input(f'\nNote: Grace Period, in days, after the password is expired that a user \n'\
                                'can continue to use their expired password.\n'\
                                'The allowed grace period is between 0 to 5 days.  With 0 being no grace period.\n\n'\
                                'How many days would you like to set for the Grace Period?  [0]: ')
                            if templateVars["grace_period"] == '':
                                templateVars["grace_period"] = 0
                            if re.fullmatch(r'[0-5]', str(templateVars["grace_period"])):
                                valid = validating_ucs.number_in_range('Grace Period', templateVars["grace_period"], 0, 5)
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter a number in the range of 0 to 5.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            templateVars["notification_period"] = input(f'Note: Notification Period - Number of days, between 0 to 15 '\
                                '(0 being disabled),\n that a user is notified to change their password before it expires.\n\n'\
                                'How many days would you like to set for the Notification Period?  [15]: ')
                            if templateVars["notification_period"] == '':
                                templateVars["notification_period"] = 15
                            if re.search(r'^[0-9]+$', str(templateVars["notification_period"])):
                                valid = validating_ucs.number_in_range('Notification Period', templateVars["notification_period"], 0, 15)
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter a number in the range of 0 to 15.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            templateVars["password_expiry_duration"] = input(f'Note: When Password Expiry is Enabled, Password Expiry Duration '\
                                'sets the duration of time,\n (in days), a password may be valid.  The password expiry duration must be greater than \n'\
                                'notification period + grace period.  Range is 1-3650.\n\n'\
                                'How many days would you like to set for the Password Expiry Duration?  [90]: ')
                            if templateVars["password_expiry_duration"] == '':
                                templateVars["password_expiry_duration"] = 90
                            if re.search(r'^[0-9]+$', str(templateVars["password_expiry_duration"])):
                                first_check = validating_ucs.number_in_range('Password Expiry Duration', templateVars["password_expiry_duration"], 1, 3650)
                                if first_check == True:
                                    x = int(templateVars["grace_period"])
                                    y = int(templateVars["notification_period"])
                                    if int(templateVars["password_expiry_duration"]) > (x + y):
                                        valid = True
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter a number in the range of 1 to 3650.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            templateVars["password_history"] = input(f'\nNote: Password change history. Specifies the number of previous passwords \n'\
                                'that are stored and compared to a new password.  Range is 0 to 5.\n\n'\
                                'How many passwords would you like to store for a user?  [5]: ')
                            if templateVars["password_history"] == '':
                                templateVars["password_history"] = 5
                            if re.fullmatch(r'[0-5]', str(templateVars["password_history"])):
                                valid = validating_ucs.number_in_range('Password History', templateVars["password_history"], 0, 5)
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter a number in the range of 0 to 5.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    else:
                        templateVars["grace_period"] = 0
                        templateVars["notification_period"] = 15
                        templateVars["password_expiry_duration"] = 90
                        templateVars["password_history"] = 5


                    templateVars["local_users"] = []
                    inner_loop_count = 1
                    user_loop = False
                    while user_loop == False:
                        question = input(f'\nWould you like to configure a Local user?  Enter "Y" or "N" [Y]: ')
                        if question == '' or question == 'Y':
                            valid_users = False
                            while valid_users == False:
                                valid = False
                                while valid == False:
                                    username = input(f'\nName of the user to be created on the endpoint. It can be any string that adheres to the following constraints:\n'\
                                        '  - It can have alphanumeric characters, dots, underscores and hyphen.\n'\
                                        '  - It cannot be more than 16 characters.\n\n'\
                                        'What is your Local username? ')
                                    if not username == '':
                                        valid = validating_ucs.username('Local User', username, 1, 16)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please Re-enter the Local Username.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                templateVars["multi_select"] = False
                                templateVars["policy_file"] = 'local_role.txt'
                                templateVars["var_description"] = '    What Role would you like to assign to this user?\n'
                                templateVars["var_type"] = 'User Role'
                                role = variable_loop(**templateVars)

                                if templateVars["enforce_strong_password"] == True:
                                    print('Enforce Strong Password is enabled so the following rules must be followed:')
                                    print('  - The password must have a minimum of 8 and a maximum of 20 characters.')
                                    print("  - The password must not contain the User's Name.")
                                    print('  - The password must contain characters from three of the following four categories.')
                                    print('    * English uppercase characters (A through Z).')
                                    print('    * English lowercase characters (a through z).')
                                    print('    * Base 10 digits (0 through 9).')
                                    print('    * Non-alphabetic characters (! , @, #, $, %, ^, &, *, -, _, +, =)\n\n')
                                valid = False
                                while valid == False:
                                    password1 = getpass.getpass(f'What is the password for {username}? ')
                                    password2 = getpass.getpass(f'Please re-enter the password for {username}? ')
                                    if not password1 == '':
                                        if password1 == password2:
                                            if templateVars["enforce_strong_password"] == True:
                                                valid = validating_ucs.strong_password(f"{username}'s password", password1, 8, 20)

                                            else:
                                                valid = validating_ucs.string_length(f'{username} password', password1, 1, 127)

                                        else:
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                            print(f'  Error!! The Passwords did not match.  Please Re-enter the password for {username}.')
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please Re-enter the password for {username}.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                TF_VAR = 'TF_VAR_local_user_password_%s' % (inner_loop_count)
                                os.environ[TF_VAR] = '%s' % (password1)
                                password1 = inner_loop_count

                                user_attributes = {
                                    'enabled':True,
                                    'password':inner_loop_count,
                                    'role':role,
                                    'username':username
                                }

                                # for k, v in os.environ.items():
                                #     print(f'key is {k}, and value is {v}')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'   enabled  = True')
                                print(f'   password = "Sensitive"')
                                print(f'   role     = "{role}"')
                                print(f'   username = "{username}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = False
                                while valid_confirm == False:
                                    confirm_v = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                                    if confirm_v == 'Y' or confirm_v == '':
                                        templateVars["local_users"].append(user_attributes)
                                        valid_exit = False
                                        while valid_exit == False:
                                            loop_exit = input(f'Would You like to Configure another Local User?  Enter "Y" or "N" [N]: ')
                                            if loop_exit == 'Y':
                                                inner_loop_count += 1
                                                valid_confirm = True
                                                valid_exit = True
                                            elif loop_exit == 'N' or loop_exit == '':
                                                user_loop = True
                                                valid_confirm = True
                                                valid_exit = True
                                                valid_users = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                    elif confirm_v == 'N':
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Starting Local User Configuration Over.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                        elif question == 'N':
                            user_loop = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    templateVars["enabled"] = True
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    always_send_user_password = {templateVars["always_send_user_password"]}')
                    print(f'    description               = "{templateVars["descr"]}"')
                    print(f'    enable_password_expiry    = {templateVars["enable_password_expiry"]}')
                    print(f'    enforce_strong_password   = {templateVars["enforce_strong_password"]}')
                    print(f'    grace_period              = "{templateVars["grace_period"]}"')
                    print(f'    name                      = "{templateVars["name"]}"')
                    print(f'    password_expiry_duration  = "{templateVars["password_expiry_duration"]}"')
                    print(f'    password_history          = "{templateVars["password_history"]}"')
                    if len(templateVars["local_users"]) > 0:
                        print(f'    local_users = ''{')
                        for item in templateVars["local_users"]:
                            for k, v in item.items():
                                if k == 'username':
                                    print(f'      "{v}" = ''{')
                            for k, v in item.items():
                                if k == 'enabled':
                                    print(f'        enable   = {v}')
                                elif k == 'password':
                                    print(f'        password = "Sensitive"')
                                elif k == 'role':
                                    print(f'        role     = {v}')
                            print(f'      ''}')
                        print(f'    ''}')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # MAC Pools Module
    #========================================
    def mac_pools(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'MAC Pool'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'mac_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  MAC Pool Convention Recommendations:')
            print(f'  - Leverage the Cisco UCS OUI of 00:25:B5 for the MAC Pool Prefix.')
            print(f'  - For MAC Pools; create a pool for each Fabric.')
            print(f'  - Pool Size can be between 1 and 1000 addresses.')
            print(f'  - Refer to "UCS Naming Conventions 0.5.ppsx" in the Repository for further guidance.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            loop_count = 0
            policy_loop = False
            while policy_loop == False:

                name = naming_rule_fabric(loop_count, name_prefix, org)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Assignment order decides the order in which the next identifier is allocated.')
                print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid = False
                while valid == False:
                    templateVars["assignment_order"] = input('Specify the number for the value to select.  [2]: ')
                    if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                        templateVars["assignment_order"] = 'sequential'
                        valid = True
                    elif templateVars["assignment_order"] == '1':
                        templateVars["assignment_order"] = 'default'
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    if loop_count % 2 == 0:
                        begin = input('What is the Beginning MAC Address to Assign to the Pool?  [00:25:B5:0A:00:00]: ')
                    else:
                        begin = input('What is the Beginning MAC Address to Assign to the Pool?  [00:25:B5:0B:00:00]: ')
                    if begin == '':
                        if loop_count % 2 == 0:
                            begin = '00:25:B5:0A:00:00'
                        else:
                            begin = '00:25:B5:0B:00:00'
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
                templateVars["mac_blocks"] = [{'from':begin, 'to':ending}]

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    assignment_order = "{templateVars["assignment_order"]}"')
                print(f'    description      = "{templateVars["descr"]}"')
                print(f'    name             = "{templateVars["name"]}"')
                print(f'    mac_blocks = [')
                for item in templateVars["mac_blocks"]:
                    print('      {')
                    for k, v in item.items():
                        if k == 'from':
                            print(f'        from = "{v}" ')
                        elif k == 'to':
                            print(f'        to   = "{v}"')
                    print('      }')
                print(f'    ]')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, loop_count, policy_loop = exit_loop_default_yes(loop_count, policy_type)

                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {policy_type} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Multicast Policy Module
    #========================================
    def multicast_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'multicast'
        org = self.org
        policy_type = 'Multicast Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'multicast_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  Each VLAN must have a Multicast Policy applied to it.  Optional attributes will be')
            print(f'  the IGMP Querier IPs.  IGMP Querier IPs are only needed if you have a non Routed VLAN')
            print(f'  and you need the Fabric Interconnects to act as IGMP Queriers for the network.')
            print(f'  If you configure IGMP Queriers for a Multicast Policy that Policy should only be')
            print(f'  Assigned to the VLAN for which those Queriers will service.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["igmp_snooping_state"] = 'Enabled'

                valid = False
                while valid == False:
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    templateVars["querier_ip_address"] = input('IGMP Querier IP for Fabric Interconnect A.  [press enter to skip] ')
                    if templateVars["querier_ip_address"] == '':
                        valid = True
                    if not templateVars["querier_ip_address"] == '':
                        valid = validating_ucs.ip_address('Fabric A IGMP Querier IP', templateVars["querier_ip_address"])

                    if not templateVars["querier_ip_address"] == '':
                        templateVars["igmp_snooping_querier_state"] == 'Enabled'
                        valid = False
                        while valid == False:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            templateVars["querier_ip_address_peer"] = input('IGMP Querier IP for Fabric Interconnect B.  [press enter to skip] ')
                            if templateVars["querier_ip_address_peer"] == '':
                                valid = True
                            if not templateVars["querier_ip_address_peer"] == '':
                                valid = validating_ucs.ip_address('Fabric B IGMP Querier IP', templateVars["querier_ip_address"])
                    else:
                        templateVars["igmp_snooping_querier_state"] = 'Disabled'
                        templateVars["querier_ip_address_peer"] = ''

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description                 = "{templateVars["descr"]}"')
                print(f'    igmp_snooping_state         = "{templateVars["igmp_snooping_state"]}"')
                print(f'    igmp_snooping_querier_state = "{templateVars["igmp_snooping_querier_state"]}"')
                print(f'    name                        = "{templateVars["name"]}"')
                if not templateVars["querier_ip_address_peer"] == '':
                    print(f'    querier_ip_address          = "{templateVars["querier_ip_address"]}"')
                    print(f'    querier_ip_address_peer     = "{templateVars["querier_ip_address_peer"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Network Connectivity Policy Module
    #========================================
    def network_connectivity_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'dns'
        org = self.org
        policy_type = 'Network Connectivity Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'network_connectivity_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  It is strongly recommended to have a Network Connectivity (DNS) Policy for the')
            print(f'  UCS Domain Profile.  Without it, DNS resolution will fail.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                valid = False
                while valid == False:
                    templateVars["preferred_ipv4_dns_server"] = input('What is your Primary IPv4 DNS Server?  [208.67.220.220]: ')
                    if templateVars["preferred_ipv4_dns_server"] == '':
                        templateVars["preferred_ipv4_dns_server"] = '208.67.220.220'
                    valid = validating_ucs.ip_address('Primary IPv4 DNS Server', templateVars["preferred_ipv4_dns_server"])

                valid = False
                while valid == False:
                    alternate_true = input('Do you want to Configure an Alternate IPv4 DNS Server?  Enter "Y" or "N" [Y]: ')
                    if alternate_true == 'Y' or alternate_true == '':
                        templateVars["alternate_ipv4_dns_server"] = input('What is your Alternate IPv4 DNS Server?  [208.67.222.222]: ')
                        if templateVars["alternate_ipv4_dns_server"] == '':
                            templateVars["alternate_ipv4_dns_server"] = '208.67.222.222'
                        valid = validating_ucs.ip_address('Alternate IPv4 DNS Server', templateVars["alternate_ipv4_dns_server"])
                    elif alternate_true == 'N':
                        templateVars["alternate_ipv4_dns_server"] = ''
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    enable_ipv6 = input('Do you want to Configure IPv6 DNS?  Enter "Y" or "N" [N]: ')
                    if enable_ipv6 == 'Y':
                        templateVars["enable_ipv6"] = True
                        templateVars["preferred_ipv6_dns_server"] = input('What is your Primary IPv6 DNS Server?  [2620:119:35::35]: ')
                        if templateVars["preferred_ipv6_dns_server"] == '':
                            templateVars["preferred_ipv6_dns_server"] = '2620:119:35::35'
                        valid = validating_ucs.ip_address('Primary IPv6 DNS Server', templateVars["preferred_ipv6_dns_server"])
                    if enable_ipv6 == 'N' or enable_ipv6 == '':
                        templateVars["enable_ipv6"] = False
                        templateVars["preferred_ipv6_dns_server"] = ''
                        valid = True

                valid = False
                while valid == False:
                    if enable_ipv6 == 'Y':
                        alternate_true = input('Do you want to Configure an Alternate IPv6 DNS Server?  Enter "Y" or "N" [Y]: ')
                        if alternate_true == 'Y' or alternate_true == '':
                            templateVars["alternate_ipv6_dns_server"] = input('What is your Alternate IPv6 DNS Server?  [2620:119:53::53]: ')
                            if templateVars["alternate_ipv6_dns_server"] == '':
                                templateVars["alternate_ipv6_dns_server"] = '2620:119:53::53'
                            valid = validating_ucs.ip_address('Alternate IPv6 DNS Server', templateVars["alternate_ipv6_dns_server"])
                        elif alternate_true == 'N':
                            templateVars["alternate_ipv6_dns_server"] = ''
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                    else:
                        templateVars["alternate_ipv6_dns_server"] = ''
                        valid = True

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description = "{templateVars["descr"]}"')
                print(f'    name        = "{templateVars["name"]}"')
                if not templateVars["preferred_ipv4_dns_server"] == '':
                    print(f'    dns_servers_v4 = [')
                    print(f'      {templateVars["preferred_ipv4_dns_server"]},')
                    if not templateVars["alternate_ipv4_dns_server"] == '':
                        print(f'      {templateVars["alternate_ipv4_dns_server"]}')
                    print(f'    ]')
                if not templateVars["preferred_ipv6_dns_server"] == '':
                    print(f'    dns_servers_v6 = [')
                    print(f'      {templateVars["preferred_ipv6_dns_server"]},')
                    if not templateVars["alternate_ipv6_dns_server"] == '':
                        print(f'      {templateVars["alternate_ipv6_dns_server"]}')
                    print(f'    ]')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # NTP Policy Module
    #========================================
    def ntp_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ntp'
        org = self.org
        policy_type = 'NTP Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_file"] = 'timezones.txt'
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ntp_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  It is strongly recommended to configure an NTP Policy for the UCS Domain Profile.')
            print(f'  Without an NTP Policy Events can be incorrectly timestamped and Intersight ')
            print(f'  Communication, as an example, could be interrupted with Certificate Validation\n')
            print(f'  checks, as an example.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

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
                    alternate_true = input('Do you want to Configure an Alternate NTP Server?  Enter "Y" or "N" [Y]: ')
                    if alternate_true == 'Y' or alternate_true == '':
                        alternate_ntp = input('What is your Alternate NTP Server? [1.north-america.pool.ntp.org]: ')
                        if alternate_ntp == '':
                            alternate_ntp = '1.north-america.pool.ntp.org'
                        if re.search(r'[a-zA-Z]+', alternate_ntp):
                            valid = validating_ucs.dns_name('Alternate NTP Server', alternate_ntp)
                        else:
                            valid = validating_ucs.ip_address('Alternate NTP Server', alternate_ntp)
                    elif alternate_true == 'N':
                        alternate_ntp = ''
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                templateVars["enabled"] = True
                templateVars["ntp_servers"] = []
                templateVars["ntp_servers"].append(primary_ntp)
                if alternate_true == 'Y' or alternate_true == '':
                    templateVars["ntp_servers"].append(alternate_ntp)

                valid = False
                while valid == False:
                    print(f'\n---------------------------------------------------------------------------------------')
                    print(f'   Timezone Regions...')
                    policy_file = 'ucs_templates/variables/%s' % (templateVars["policy_file"])
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
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

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
                            templateVars["timezone"] = v
                            valid = True
                    if valid == False:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                    template_file.close()

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description = "{templateVars["descr"]}"')
                print(f'    name        = "{templateVars["name"]}"')
                print(f'    timezone    = "{templateVars["timezone"]}"')
                if len(templateVars["ntp_servers"]) > 0:
                    print(f'    ntp_servers = [')
                    for server in templateVars["ntp_servers"]:
                        print(f'      "{server}",')
                    print(f'    ]')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Persistent Memory Policy Module
    #========================================
    def persistent_memory_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'persistent_memory'
        org = self.org
        policy_type = 'Persistent Memory Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'persistent_memory_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} allows the configuration of security, Goals, and ')
            print(f'  Namespaces of Persistent Memory Modules:')
            print(f'  - Goal - Used to configure volatile memory and regions in all the PMem Modules connected ')
            print(f'    to all the sockets of the server. Intersight supports only the creation and modification')
            print(f'    of a Goal as part of the Persistent Memory policy. Some data loss occurs when a Goal is')
            print(f'    modified during the creation or modification of a Persistent Memory Policy.')
            print(f'  - Namespaces - Used to partition a region mapped to a specific socket or a PMem Module on a')
            print(f'    socket.  Intersight supports only the creation and deletion of Namespaces as part of the ')
            print(f'    Persistent Memory Policy. Modifying a Namespace is not supported. Some data loss occurs ')
            print(f'    when a Namespace is created or deleted during the creation of a Persistent Memory policy.')
            print(f'    It is important to consider the memory performance guidelines and population rules of ')
            print(f'    the Persistent Memory Modules before they are installed or replaced, and the policy is ')
            print(f'    deployed. The population guidelines for the PMem Modules can be divided into the  ')
            print(f'    following categories, based on the number of CPU sockets:')
            print(f'    * Dual CPU for UCS B200 M6, C220 M6, C240 M6, and xC210 M6 servers')
            print(f'    * Dual CPU for UCS C220 M5, C240 M5, and B200 M5 servers')
            print(f'    * Dual CPU for UCS S3260 M5 servers')
            print(f'    * Quad CPU for UCS C480 M5 and B480 M5 servers')
            print(f'  - Security - Used to configure the secure passphrase for all the persistent memory modules.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'persistent_management_mode.txt'
                    templateVars["var_description"] = '    Management Mode of the policy.\n'\
                        '    - configured-from-intersight - (Default) The Persistent Memory Modules are configured \n'\
                        '      from Intersight thorugh Persistent Memory policy.\n'\
                        '    - configured-from-operating-system - The Persistent Memory Modules are configured \n'\
                        '      from operating system thorugh OS tools.\n'
                    templateVars["var_type"] = 'Management Mode'
                    templateVars["management_mode"] = variable_loop(**templateVars)
                    if templateVars["management_mode"] == 'configured-from-intersight':
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  A Secure passphrase will enable the protection of data on the persistent memory modules. ')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        valid = False
                        while valid == False:
                            encrypt_memory = input('Do you want to enable a secure passphrase?  Enter "Y" or "N" [Y]: ')
                            if encrypt_memory == 'Y' or encrypt_memory == '':
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  The Passphrase must be between 8 and 32 characters in length.  The allowed characters are:')
                                print(f'   - a-z, A-Z, 0-9 and special characters: \u0021, &, #, $, %, +, ^, @, _, *, -.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_passphrase = False
                                while valid_passphrase == False:
                                    secure_passphrase = getpass.getpass(prompt='Enter the Secure Passphrase: ')
                                    minLength = 8
                                    maxLength = 32
                                    rePattern = '^[a-zA-Z0-9\\u0021\\&\\#\\$\\%\\+\\%\\@\\_\\*\\-\\.]+$'
                                    varName = 'Secure Passphrase'
                                    varValue = secure_passphrase
                                    valid_passphrase = validating_ucs.length_and_regex_sensitive(rePattern, varName, varValue, minLength, maxLength)

                                os.environ['TF_VAR_secure_passphrase'] = '%s' % (secure_passphrase)
                                valid = True
                            else:
                                valid = True

                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  The percentage of volatile memory required for goal creation.')
                        print(f'  The actual volatile and persistent memory size allocated to the region may differ with')
                        print(f'  the given percentage.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        valid = False
                        while valid == False:
                            templateVars["memory_mode_percentage"] = input('What is the Percentage of Valatile Memory to assign to this Policy?  [0]: ')
                            if templateVars["memory_mode_percentage"] == '':
                                templateVars["memory_mode_percentage"] = 0
                            if re.search(r'[\d]+', str(templateVars["memory_mode_percentage"])):
                                valid = validating_ucs.number_in_range('Memory Mode Percentage', templateVars["memory_mode_percentage"], 1, 100)
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  "{templateVars["memory_mode_percentage"]}" is not a valid number.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'persistent_memory_type.txt'
                        templateVars["var_description"] = '   Type of the Persistent Memory configuration where the Persistent Memory Modules\n'\
                            '    are combined in an interleaved set or not.\n'\
                            '    - app-direct - (Default) The App Direct interleaved Persistent Memory type.\n'\
                            '    - app-direct-non-interleaved - The App Direct non-interleaved Persistent Memory type.\n\n'
                        templateVars["var_type"] = 'Persistent Memory Type'
                        templateVars["persistent_memory_type"] = variable_loop(**templateVars)

                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  This Flag will enable or Disable the retention of Namespaces between Server Profile')
                        print(f'  association and dissassociation.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        valid = False
                        while valid == False:
                            templateVars["retain_namespaces"] = input('Do you want to Retain Namespaces?  Enter "Y" or "N" [Y]: ')
                            if templateVars["retain_namespaces"] == '' or templateVars["retain_namespaces"] == 'Y':
                                templateVars["retain_namespaces"] = True
                                valid = True
                            elif templateVars["retain_namespaces"] == 'N':
                                templateVars["retain_namespaces"] = False
                                valid = True
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        templateVars["namespaces"] = []
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Namespace is a partition made in one or more Persistent Memory Regions. You can create a')
                        print(f'  namespace in Raw or Block mode.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        namespace_configure = input(f'Do You Want to Configure a namespace?  Enter "Y" or "N" [Y]: ')
                        if namespace_configure == 'Y' or namespace_configure == '':
                            sub_loop = False
                            while sub_loop == False:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Name of this Namespace to be created on the server.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid = False
                                while valid == False:
                                    namespace_name = input('What is the Name for this Namespace? ')
                                    minLength = 1
                                    maxLength = 63
                                    rePattern = '^[a-zA-Z0-9\\#\\_\\-]+$'
                                    varName = 'Name for the Namespace'
                                    varValue = namespace_name
                                    valid = validating_ucs.length_and_regex(rePattern, varName, varValue, minLength, maxLength)

                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Capacity of this Namespace in gibibytes (GiB).  Range is 1-9223372036854775807')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid = False
                                while valid == False:
                                    capacity = input('What is the Capacity to assign to this Namespace? ')
                                    minLength = 1
                                    maxLength = 9223372036854775807
                                    varName = 'Namespace Capacity'
                                    varValue = capacity
                                    if re.search(r'[\d]+',str(varName)):
                                        valid = validating_ucs.number_in_range(varName, varValue, minLength, maxLength)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  "{varValue}" is not a valid number.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                templateVars["multi_select"] = False
                                templateVars["policy_file"] = 'persistent_namespace_mode.txt'
                                templateVars["var_description"] = '   Mode of this Namespace.\n'\
                                    '    - block - A Namespace created in Block mode is seen as a sector mode Namespace in the host OS.\n'\
                                    '    - raw - (Default) A Namespace created in Raw mode is seen as a raw mode Namespace in the host OS.\n\n'
                                templateVars["var_type"] = 'Mode'
                                mode = variable_loop(**templateVars)

                                templateVars["multi_select"] = False
                                templateVars["policy_file"] = 'persistent_namespace_socket_id.txt'
                                templateVars["var_description"] = '   Socket ID of the region on which this Namespace will apply.\n'\
                                    '    - 1 - The first CPU socket in a server.\n'\
                                    '    - 2 - The second CPU socket in a server.\n'\
                                    '    - 3 - The third CPU socket in a server.\n'\
                                    '    - 4 - The fourth CPU socket in a server.\n\n'
                                templateVars["var_type"] = 'Mode'
                                socket_id = variable_loop(**templateVars)

                                if templateVars["persistent_memory_type"] == 'app-direct-non-interleaved':
                                    templateVars["multi_select"] = False
                                    templateVars["policy_file"] = 'persistent_namespace_socket_memory_id.txt'
                                    templateVars["var_description"] = '   Socket Memory ID of the region on which this Namespace will apply.\n'\
                                        '    - 2 - The second socket memory ID within a socket in a server.\n'\
                                        '    - 4 - The fourth socket memory ID within a socket in a server.\n'\
                                        '    - 6 - The sixth socket memory ID within a socket in a server.\n'\
                                        '    - 8 - The eight socket memory ID within a socket in a server.\n'\
                                        '    - 10 - The tenth socket memory ID within a socket in a server.\n'\
                                        '    - 12 - The twelfth socket memory ID within a socket in a server.\n\n'
                                    templateVars["var_type"] = 'Mode'
                                    socket_memory_id = variable_loop(**templateVars)
                                else:
                                    socket_memory_id = 'Not Applicable'

                                namespace = {
                                    'capacity':capacity,
                                    'mode':mode,
                                    'name':namespace_name,
                                    'socket_id':socket_id,
                                    'socket_memory_id':socket_memory_id
                                }
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'   capacity         = "{capacity}"')
                                print(f'   mode             = "{mode}"')
                                print(f'   name             = "{namespace_name}"')
                                print(f'   socket_id        = "{socket_id}"')
                                print(f'   socket_memory_id = "{socket_memory_id}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = False
                                while valid_confirm == False:
                                    confirm_namespace = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                    if confirm_namespace == 'Y' or confirm_namespace == '':
                                        templateVars["namespaces"].append(namespace)

                                        valid_exit = False
                                        while valid_exit == False:
                                            sub_exit = input(f'Would You like to Configure another namespace?  Enter "Y" or "N" [N]: ')
                                            if sub_exit == 'Y':
                                                valid_confirm = True
                                                valid_exit = True
                                            elif sub_exit == 'N' or sub_exit == '':
                                                sub_loop = True
                                                valid = True
                                                valid_confirm = True
                                                valid_exit = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                    elif confirm_namespace == 'N':
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Starting namespace Configuration Over.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'    description     = "{templateVars["descr"]}"')
                    print(f'    management_mode = {templateVars["management_mode"]}')
                    print(f'    name            = {templateVars["name"]}')
                    if templateVars["management_mode"]  == 'configured-from-intersight':
                        print(f'    # GOALS')
                        print(f'    memory_mode_percentage = {templateVars["memory_mode_percentage"]}')
                        print(f'    persistent_memory_type = {templateVars["persistent_memory_type"]}')
                        print(f'    # NAMESPACES')
                        print(f'    namespaces = ''{')
                        for item in templateVars["namespaces"]:
                            for k, v in item.items():
                                if k == 'name':
                                    print(f'      "{v}" = ''{')
                            for k, v in item.items():
                                if k == 'capacity':
                                    print(f'        capacity         = {v}')
                                elif k == 'mode':
                                    print(f'        mode             = {v}')
                                elif k == 'socket_id':
                                    print(f'        socket_id        = {v}')
                                elif k == 'socket_memory_id':
                                    print(f'        socket_memory_id = {v}')
                            print(f'      ''}')
                        print(f'    ''}')
                        print(f'   retain_namespaces = "{templateVars["retain_namespaces"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Port Policy Module
    #========================================
    def port_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'Port Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'port_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        port_count = 0
        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} is used to configure the ports for a UCS Domain Profile.  This includes:')
            print(f'   - Unified Ports - Ports to convert to Fibre-Channel Mode.')
            print(f'   - Appliance Ports')
            print(f'   - Appliance Port-Channels')
            print(f'   - Ethernet Uplinks')
            print(f'   - Ethernet Uplink Port-Channels')
            print(f'   - FCoE Uplinks')
            print(f'   - FCoE Uplink Port-Channels')
            print(f'   - Fibre-Channel Uplinks')
            print(f'   - Fibre-Channel Uplink Port-Channels')
            print(f'   - Server Ports\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                print(f'   IMPORTANT NOTE: The wizard will create a Port Policy for Fabric A and Fabric B')
                print(f'                   automatically.  The Policy Name will be appended with [name]_A for ')
                print(f'                   Fabric A and [name]_B for Fabric B.  You only need one Policy per')
                print(f'                   Domain.')
                print(f'\n-------------------------------------------------------------------------------------------\n')

                if not name_prefix == '':
                    name = '%s' % (name_prefix)
                else:
                    name = '%s' % (org)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'device_model.txt'
                templateVars["var_description"] = '    Please Choose the model of Fabric Interconnect to configure:\n'
                templateVars["var_type"] = 'Model'
                model = variable_loop(**templateVars)
                templateVars["device_model"] = model

                fc_mode = ''
                ports_in_use = []
                fc_converted_ports = []
                valid = False
                while valid == False:
                    fc_mode = input('Do you want to convert ports to Fibre Channel Mode?  Enter "Y" or "N" [Y]: ')
                    if fc_mode == '' or fc_mode == 'Y':
                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'unified_ports.txt'
                        templateVars["var_description"] = '    Please Select the Port Range to convert to Fibre-Channel Mode:\n'
                        templateVars["var_type"] = 'Unified Ports'
                        fc_ports = variable_loop(**templateVars)
                        x = fc_ports.split('-')
                        fc_ports = [int(x[0]),int(x[1])]
                        for i in range(int(x[0]), int(x[1]) + 1):
                            ports_in_use.append(i)
                            fc_converted_ports.append(i)
                        templateVars["port_modes"] = {'custom_mode':'FibreChannel','port_list':fc_ports,'slot_id':1}
                        valid = True
                    elif fc_mode == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_channel_appliances = []
                port_type = 'Appliance Port-Channel'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure an {port_type}?  Enter "Y" or "N" [N]: ')
                    if configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [95,96]: ')
                            else:
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [47,48]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '95,96'
                            elif port_list == '':
                                port_list = '47,48'
                            port_group = []
                            if re.search(r'(^[0-9]+$)', port_list):
                                port_group.append(port_list)
                            elif re.search(r'(^[0-9]+,{1,16}[0-9]+$)', port_list):
                                x = port_list.split(',')
                                port_group = []
                                for i in x:
                                    port_group.append(i)
                            if re.search(r'(^[0-9]+$|^[0-9]+,{1,16}[0-9]+$)', port_list):
                                port_list = port_group
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'ethernet_admin_speed.txt'
                                        templateVars["var_description"] = '    Please Select the Admin Speed for the Port-Channel:\n'
                                        templateVars["var_type"] = 'Admin Speed'
                                        admin_speed = variable_loop(**templateVars)

                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'port_mode.txt'
                                        templateVars["var_description"] = '    Please Select the Port Mode:\n'
                                        templateVars["var_type"] = 'Port Mode'
                                        templateVars["mode"] = variable_loop(**templateVars)

                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'qos_priority.txt'
                                        templateVars["var_description"] = '   Priority:  Default is "Best Effort".\n   The Priority Queue to Assign to this Port:\n'
                                        templateVars["var_type"] = 'Priority'
                                        templateVars["priority"] = variable_loop(**templateVars)

                                        # Prompt User for the
                                        policy_list = [
                                            'policies.ethernet_network_control_policies.ethernet_network_control_policy',
                                            'policies.ethernet_network_group_policies.ethernet_network_group_policy',
                                        ]
                                        templateVars["allow_opt_out"] = False
                                        for policy in policy_list:
                                            policy_short = policy.split('.')[2]
                                            templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                            templateVars.update(policyData)

                                        interfaces = []
                                        for i in port_list:
                                            interfaces.append({'port_id':i,'slot_id':1})

                                        pc_id = port_list[0]
                                        port_channel = {
                                            'admin_speed':admin_speed,
                                            'ethernet_network_control_policy':templateVars["ethernet_network_control_policy"],
                                            'ethernet_network_group_policy':templateVars["ethernet_network_group_policy"],
                                            'interfaces':interfaces,
                                            'mode':templateVars["mode"],
                                            'pc_id':pc_id,
                                            'priority':templateVars["priority"],
                                            'slot_id':1
                                        }
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following configuration?')
                                        print(f'    admin_speed                     = "{admin_speed}"')
                                        print(f'    ethernet_network_control_policy = "{templateVars["ethernet_network_control_policy"]}"')
                                        print(f'    ethernet_network_group_policy   = "{templateVars["ethernet_network_group_policy"]}"')
                                        print(f'    interfaces = [')
                                        for item in interfaces:
                                            print('      {')
                                            for k, v in item.items():
                                                print(f'        {k}          = {v}')
                                            print('      }')
                                        print(f'    ]')
                                        print(f'    mode         = "{templateVars["mode"]}"')
                                        print(f'    priority     = "{templateVars["priority"]}"')
                                        print(f'    pc_id        = {pc_id}')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                port_channel_appliances.append(port_channel)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == '' or configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_channel_ethernet_uplinks = []
                port_type = 'Ethernet Uplink Port-Channel'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure an {port_type}?  Enter "Y" or "N" [Y]: ')
                    if configure_port == '' or configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [97,98]: ')
                            else:
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [49,50]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '97,98'
                            elif port_list == '':
                                port_list = '49,50'
                            port_group = []
                            if re.search(r'(^[0-9]+$)', port_list):
                                port_group.append(port_list)
                            elif re.search(r'(^[0-9]+,{1,16}[0-9]+$)', port_list):
                                x = port_list.split(',')
                                port_group = []
                                for i in x:
                                    port_group.append(i)
                            if re.search(r'(^[0-9]+$|^[0-9]+,{1,16}[0-9]+$)', port_list):
                                port_list = port_group
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'ethernet_admin_speed.txt'
                                        templateVars["var_description"] = '    Please Select the Admin Speed for the Port-Channel:\n'
                                        templateVars["var_type"] = 'Admin Speed'
                                        admin_speed = variable_loop(**templateVars)

                                        # Prompt User for the
                                        policy_list = [
                                            'policies.flow_control_policies.flow_control_policy',
                                            'policies.link_aggregation_policies.link_aggregation_policy',
                                            'policies.link_control_policies.link_control_policy',
                                        ]
                                        templateVars["allow_opt_out"] = True
                                        for policy in policy_list:
                                            policy_short = policy.split('.')[2]
                                            templateVars[policy_short],
                                            policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                            templateVars.update(policyData)

                                        interfaces = []
                                        for i in port_list:
                                            interfaces.append({'port_id':i,'slot_id':1})

                                        pc_id = port_list[0]
                                        port_channel = {
                                            'admin_speed':admin_speed,
                                            'flow_control_policy':templateVars["flow_control_policy"],
                                            'interfaces':interfaces,
                                            'link_aggregation_policy':templateVars["link_aggregation_policy"],
                                            'link_control_policy':templateVars["link_control_policy"],
                                            'pc_id':pc_id,
                                            'slot_id':1
                                        }
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following configuration?')
                                        print(f'    admin_speed             = "{admin_speed}"')
                                        print(f'    flow_control_policy     = "{templateVars["flow_control_policy"]}"')
                                        print(f'    interfaces = [')
                                        for item in interfaces:
                                            print('      {')
                                            for k, v in item.items():
                                                print(f'        {k}          = {v}')
                                            print('      }')
                                        print(f'    ]')
                                        print(f'    link_aggregation_policy = "{templateVars["link_aggregation_policy"]}"')
                                        print(f'    link_control_policy     = "{templateVars["link_control_policy"]}"')
                                        print(f'    pc_id                   = {pc_id}')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                port_channel_ethernet_uplinks.append(port_channel)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                fc_ports_in_use = []
                Fabric_A_fc_port_channels = []
                Fabric_B_fc_port_channels = []
                port_type = 'Fibre Channel Port-Channel'
                valid = False
                while valid == False:
                    if len(fc_converted_ports) > 0:
                        configure_port = input(f'Do you want to configure a {port_type}?  Enter "Y" or "N" [Y]: ')
                    else:
                        configure_port = 'N'
                        valid = True
                    if configure_port == '' or configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            templateVars["multi_select"] = True
                            templateVars["port_type"] = port_type
                            templateVars["var_description"] = '    Please Select a Port for the Port-Channel:\n'
                            templateVars["var_type"] = 'Unified Port'
                            port_list = vars_from_list(fc_converted_ports, **templateVars)

                            # Prompt User for the Admin Speed of the Port
                            templateVars["multi_select"] = False
                            templateVars["policy_file"] = 'fc_admin_speed.txt'
                            templateVars["var_description"] = '    Please Select the Admin Speed for the Port-Channel:\n'
                            templateVars["var_type"] = 'Admin Speed'
                            admin_speed = variable_loop(**templateVars)

                            # Prompt User for the Admin Speed of the Port
                            templateVars["multi_select"] = False
                            templateVars["policy_file"] = 'fill_pattern.txt'
                            templateVars["var_description"] = '    Please Select the Fill Pattern for the Uplink:\n'\
                                'For Cisco UCS 6400 Series fabric interconnect, if the FC uplink speed is 8 Gbps, set the \n'\
                                'fill pattern as IDLE on the uplink switch. If the fill pattern is not set as IDLE, FC \n'\
                                'uplinks operating at 8 Gbps might go to an errDisabled state, lose SYNC intermittently, or \n'\
                                'notice errors or bad packets.  For speeds greater than 8 Gbps we recommend Arbff.  Below\n'\
                                'is a configuration example on MDS to match this setting:\n\n'\
                                'mds-a(config-if)# switchport fill-pattern IDLE speed 8000\n'\
                                'mds-a(config-if)# show port internal inf interface fc1/1 | grep FILL\n'\
                                '  FC_PORT_CAP_FILL_PATTERN_8G_CHANGE_CAPABLE (1)\n'\
                                'mds-a(config-if)# show run int fc1/16 | incl fill\n\n'\
                                'interface fc1/16\n'\
                                '  switchport fill-pattern IDLE speed 8000\n\n'\
                                'mds-a(config-if)#\n'
                            templateVars["var_type"] = 'Fill Pattern'
                            fill_pattern = variable_loop(**templateVars)

                            vsans = {}
                            fabrics = ['Fabric_A', 'Fabric_B']
                            for fabric in fabrics:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Please Select the VSAN Policy for {fabric}')
                                policy_list = [
                                    'policies.vsan_policies.vsan_policy',
                                ]
                                templateVars["allow_opt_out"] = False
                                for policy in policy_list:
                                    vsan_policy,policyData = policy_select_loop(name_prefix, policy, **templateVars)

                                vsan_list = []
                                for item in policyData['vsan_policies']:
                                    for key, value in item.items():
                                        if key == vsan_policy:
                                            for i in value[0]['vlans']:
                                                for k, v in i.items():
                                                    for x in v:
                                                        for y, val in x.items():
                                                            if y == 'vlan_list':
                                                                vsan_list.append(val)

                                vsan_list = ','.join(vsan_list)
                                vsan_list = vlan_list_full(vsan_list)

                                templateVars["multi_select"] = False
                                templateVars["port_type"] = port_type
                                templateVars["var_description"] = '    Please Select a VSAN for the Port-Channel:\n'
                                templateVars["var_type"] = 'VSAN'
                                vsan_x = vars_from_list(vsan_list, **templateVars)
                                for vs in vsan_x:
                                    vsan = vs
                                vsans.update({fabric:vsan})


                            interfaces = []
                            for i in port_list:
                                interfaces.append({'port_id':i,'slot_id':1})

                            pc_id = port_list[0]
                            port_channel_a = {
                                'admin_speed':admin_speed,
                                'fill_pattern':fill_pattern,
                                'interfaces':interfaces,
                                'pc_id':pc_id,
                                'slot_id':1,
                                'vsan_id':vsans.get("Fabric_A")
                            }
                            port_channel_b = {
                                'admin_speed':admin_speed,
                                'fill_pattern':fill_pattern,
                                'interfaces':interfaces,
                                'pc_id':pc_id,
                                'slot_id':1,
                                'vsan_id':vsans.get("Fabric_B")
                            }
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Do you want to accept the following configuration?')
                            print(f'    admin_speed  = "{admin_speed}"')
                            print(f'    fill_pattern = "{fill_pattern}"')
                            print(f'    interfaces = [')
                            for item in interfaces:
                                print('      {')
                                for k, v in item.items():
                                    print(f'        {k}          = {v}')
                                print('      }')
                            print(f'    ]')
                            print(f'    vsan_id_fabric_a = {vsans.get("Fabric_A")}')
                            print(f'    vsan_id_fabric_b = {vsans.get("Fabric_B")}')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            valid_confirm = False
                            while valid_confirm == False:
                                confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                if confirm_port == 'Y' or confirm_port == '':
                                    Fabric_A_fc_port_channels.append(port_channel_a)
                                    Fabric_B_fc_port_channels.append(port_channel_b)
                                    for i in port_list:
                                        fc_ports_in_use.append(i)

                                    valid_exit = False
                                    while valid_exit == False:
                                        port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                        if port_exit == 'Y':
                                            port_count += 1
                                            valid_confirm = True
                                            valid_exit = True
                                        elif port_exit == 'N' or port_exit == '':
                                            configure_valid = True
                                            valid = True
                                            valid_confirm = True
                                            valid_exit = True
                                        else:
                                            print(f'\n------------------------------------------------------\n')
                                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                            print(f'\n------------------------------------------------------\n')

                                elif confirm_port == 'N':
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Starting {port_type} Configuration Over.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    valid_confirm = True
                                else:
                                    print(f'\n------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                    print(f'\n------------------------------------------------------\n')

                    elif configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_channel_fcoe_uplinks = []
                port_type = 'FCoE Uplink Port-Channel'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure an {port_type}?  Enter "Y" or "N" [N]: ')
                    if configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [97,98]: ')
                            else:
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [49,50]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '97,98'
                            elif port_list == '':
                                port_list = '49,50'
                            port_group = []
                            if re.search(r'(^[0-9]+$)', port_list):
                                port_group.append(port_list)
                            elif re.search(r'(^[0-9]+,{1,16}[0-9]+$)', port_list):
                                x = port_list.split(',')
                                port_group = []
                                for i in x:
                                    port_group.append(i)
                            if re.search(r'(^[0-9]+$|^[0-9]+,{1,16}[0-9]+$)', port_list):
                                port_list = port_group
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'ethernet_admin_speed.txt'
                                        templateVars["var_description"] = '    Please Select the Admin Speed for the Port-Channel:\n'
                                        templateVars["var_type"] = 'Admin Speed'
                                        admin_speed = variable_loop(**templateVars)

                                        # Prompt User for the
                                        policy_list = [
                                            'policies.link_aggregation_policies.link_aggregation_policy',
                                            'policies.link_control_policies.link_control_policy',
                                        ]
                                        templateVars["allow_opt_out"] = True
                                        for policy in policy_list:
                                            policy_short = policy.split('.')[2]
                                            templateVars[policy_short],
                                            policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                            templateVars.update(policyData)

                                        interfaces = []
                                        for i in port_list:
                                            interfaces.append({'port_id':i,'slot_id':1})

                                        pc_id = port_list[0]
                                        port_channel = {
                                            'admin_speed':admin_speed,
                                            'interfaces':interfaces,
                                            'link_aggregation_policy':templateVars["link_aggregation_policy"],
                                            'link_control_policy':templateVars["link_control_policy"],
                                            'pc_id':pc_id,
                                            'slot_id':1
                                        }
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following configuration?')
                                        print(f'    admin_speed             = "{admin_speed}"')
                                        print(f'    interfaces = [')
                                        for item in interfaces:
                                            print('      {')
                                            for k, v in item.items():
                                                print(f'        {k}          = {v}')
                                            print('      }')
                                        print(f'    ]')
                                        print(f'    link_aggregation_policy = "{templateVars["link_aggregation_policy"]}"')
                                        print(f'    link_control_policy     = "{templateVars["link_control_policy"]}"')
                                        print(f'    pc_id                   = {pc_id}')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                port_channel_fcoe_uplinks.append(port_channel)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == '' or configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_role_appliances = []
                port_type = 'Appliance Ports'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure an {port_type}?  Enter "Y" or "N" [N]: ')
                    if configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5-10 - Range of Ports')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'     5-10,20-30 - Ranges and Lists of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the ports you want to add to the {port_type}?  [94]: ')
                            else:
                                port_list = input(f'Please enter the ports you want to add to the {port_type}?  [46]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '94'
                            elif port_list == '':
                                port_list = '46'
                            if re.search(r'(^\d+$|^\d+,{1,48}\d+$|^(\d+\-\d+|\d,){1,48}\d+$)', port_list):
                                original_port_list = port_list
                                ports_expanded = vlan_list_full(port_list)
                                port_list = ports_expanded
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'ethernet_admin_speed.txt'
                                        templateVars["var_description"] = '    Please Select the Admin Speed for the Port:\n'
                                        templateVars["var_type"] = 'Admin Speed'
                                        admin_speed = variable_loop(**templateVars)

                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'fec.txt'
                                        templateVars["var_description"] = '    Forward error correction configuration for the port:\n'\
                                            '    - Auto - (Default).  Forward error correction option Auto.\n'\
                                            '    - Cl91 - Forward error correction option cl91\n'\
                                            '    - Cl74 - Forward error correction option cl74.\n'
                                        templateVars["var_type"] = 'FEC'
                                        fec = variable_loop(**templateVars)

                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'port_mode.txt'
                                        templateVars["var_description"] = '    Please Select the Port Mode:\n'
                                        templateVars["var_type"] = 'Port Mode'
                                        templateVars["mode"] = variable_loop(**templateVars)

                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'qos_priority.txt'
                                        templateVars["var_description"] = '   Priority:  Default is "Best Effort".\n   The Priority Queue to Assign to this Port:\n'
                                        templateVars["var_type"] = 'Priority'
                                        templateVars["priority"] = variable_loop(**templateVars)

                                        # Prompt User for the
                                        policy_list = [
                                            'policies.ethernet_network_control_policies.ethernet_network_control_policy',
                                            'policies.ethernet_network_group_policies.ethernet_network_group_policy',
                                        ]
                                        templateVars["allow_opt_out"] = False
                                        for policy in policy_list:
                                            policy_short = policy.split('.')[2]
                                            templateVars[policy_short],
                                            policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                            templateVars.update(policyData)

                                        port_role = {
                                            'admin_speed':admin_speed,
                                            'ethernet_network_control_policy':templateVars["ethernet_network_control_policy"],
                                            'ethernet_network_group_policy':templateVars["ethernet_network_group_policy"],
                                            'fec':fec,
                                            'mode':templateVars["mode"],
                                            'port_id':original_port_list,
                                            'priority':templateVars["priority"],
                                            'slot_id':1
                                        }
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following configuration?')
                                        print(f'    admin_speed                     = "{admin_speed}"')
                                        print(f'    ethernet_network_control_policy = "{templateVars["ethernet_network_control_policy"]}"')
                                        print(f'    ethernet_network_group_policy   = "{templateVars["ethernet_network_group_policy"]}"')
                                        print(f'    fec                             = "{fec}"')
                                        print(f'    mode                            = "{templateVars["mode"]}"')
                                        print(f'    port_list                       = "{original_port_list}"')
                                        print(f'    priority                        = "{templateVars["priority"]}"')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                port_role_appliances.append(port_role)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == '' or configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_role_ethernet_uplinks = []
                port_type = 'Ethernet Uplink'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure an {port_type}?  Enter "Y" or "N" [Y]: ')
                    if configure_port == '' or configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5-10 - Range of Ports')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'     5-10,20-30 - Ranges and Lists of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [97]: ')
                            else:
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [49]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '97'
                            elif port_list == '':
                                port_list = '49'
                            if re.search(r'(^\d+$|^\d+,{1,48}\d+$|^(\d+\-\d+|\d,){1,48}\d+$)', port_list):
                                original_port_list = port_list
                                ports_expanded = vlan_list_full(port_list)
                                port_list = ports_expanded
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'ethernet_admin_speed.txt'
                                        templateVars["var_description"] = '    Please Select the Admin Speed for the Port:\n'
                                        templateVars["var_type"] = 'Admin Speed'
                                        admin_speed = variable_loop(**templateVars)

                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'fec.txt'
                                        templateVars["var_description"] = '    Forward error correction configuration for the port:\n'\
                                            '    - Auto - (Default).  Forward error correction option Auto.\n'\
                                            '    - Cl91 - Forward error correction option cl91\n'\
                                            '    - Cl74 - Forward error correction option cl74.\n'
                                        templateVars["var_type"] = 'FEC'
                                        fec = variable_loop(**templateVars)

                                        # Prompt User for the
                                        policy_list = [
                                            'policies.flow_control_policies.flow_control_policy',
                                            'policies.link_control_policies.link_control_policy',
                                        ]
                                        templateVars["allow_opt_out"] = True
                                        for policy in policy_list:
                                            policy_short = policy.split('.')[2]
                                            templateVars[policy_short],
                                            policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                            templateVars.update(policyData)

                                        port_role = {
                                            'admin_speed':admin_speed,
                                            'fec':fec,
                                            'flow_control_policy':templateVars["flow_control_policy"],
                                            'link_control_policy':templateVars["link_control_policy"],
                                            'port_id':original_port_list,
                                            'slot_id':1
                                        }
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following configuration?')
                                        print(f'    admin_speed         = "{admin_speed}"')
                                        print(f'    fec                 = "{fec}"')
                                        print(f'    flow_control_policy = "{templateVars["flow_control_policy"]}"')
                                        print(f'    link_control_policy = "{templateVars["link_control_policy"]}"')
                                        print(f'    port_list           = "{original_port_list}"')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                port_role_ethernet_uplinks.append(port_role)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                Fabric_A_port_role_fc = []
                Fabric_B_port_role_fc = []
                port_type = 'Fibre-Channel Uplink'
                valid = False
                while valid == False:
                    if len(fc_converted_ports) > 0:
                        configure_port = input(f'Do you want to configure a {port_type}?  Enter "Y" or "N" [Y]: ')
                    else:
                        configure_port = 'N'
                        valid = True
                    if configure_port == '' or configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            templateVars["multi_select"] = False
                            templateVars["port_type"] = port_type
                            templateVars["var_description"] = '    Please Select a Port for the Uplink:\n'
                            templateVars["var_type"] = 'Unified Port'
                            port_list = vars_from_list(fc_converted_ports, **templateVars)

                            # Prompt User for the Admin Speed of the Port
                            templateVars["multi_select"] = False
                            templateVars["policy_file"] = 'fc_admin_speed.txt'
                            templateVars["var_description"] = '    Please Select the Admin Speed for the Uplink:\n'
                            templateVars["var_type"] = 'Admin Speed'
                            admin_speed = variable_loop(**templateVars)

                            # Prompt User for the Admin Speed of the Port
                            templateVars["multi_select"] = False
                            templateVars["policy_file"] = 'fill_pattern.txt'
                            templateVars["var_description"] = '    Please Select the Fill Pattern for the Uplink:\n'\
                                'For Cisco UCS 6400 Series fabric interconnect, if the FC uplink speed is 8 Gbps, set the \n'\
                                'fill pattern as IDLE on the uplink switch. If the fill pattern is not set as IDLE, FC \n'\
                                'uplinks operating at 8 Gbps might go to an errDisabled state, lose SYNC intermittently, or \n'\
                                'notice errors or bad packets.  For speeds greater than 8 Gbps we recommend Arbff.  Below\n'\
                                'is a configuration example on MDS to match this setting:\n\n'\
                                'mds-a(config-if)# switchport fill-pattern IDLE speed 8000\n'\
                                'mds-a(config-if)# show port internal inf interface fc1/1 | grep FILL\n'\
                                '  FC_PORT_CAP_FILL_PATTERN_8G_CHANGE_CAPABLE (1)\n'\
                                'mds-a(config-if)# show run int fc1/16 | incl fill\n\n'\
                                'interface fc1/16\n'\
                                '  switchport fill-pattern IDLE speed 8000\n\n'\
                                'mds-a(config-if)#\n'
                            templateVars["var_type"] = 'Fill Pattern'
                            fill_pattern = variable_loop(**templateVars)

                            vsans = {}
                            fabrics = ['Fabric_A', 'Fabric_B']
                            for fabric in fabrics:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Please Select the VSAN Policy for {fabric}')
                                policy_list = [
                                    'policies.vsan_policies.vsan_policy',
                                ]
                                templateVars["allow_opt_out"] = False
                                for policy in policy_list:
                                    vsan_policy,policyData = policy_select_loop(name_prefix, policy, **templateVars)

                                vsan_list = []
                                for item in policyData['vsan_policies']:
                                    for key, value in item.items():
                                        if key == vsan_policy:
                                            for i in value[0]['vlans']:
                                                for k, v in i.items():
                                                    for x in v:
                                                        for y, val in x.items():
                                                            if y == 'vlan_list':
                                                                vsan_list.append(val)

                                vsan_list = ','.join(vsan_list)
                                vsan_list = vlan_list_full(vsan_list)

                                templateVars["multi_select"] = False
                                templateVars["port_type"] = port_type
                                templateVars["var_description"] = '    Please Select a VSAN for the Port-Channel:\n'
                                templateVars["var_type"] = 'VSAN'
                                vsan_x = vars_from_list(vsan_list, **templateVars)
                                for vs in vsan_x:
                                    vsan = vs
                                vsans.update({fabric:vsan})

                            port_list = '%s' % (port_list[0])
                            fc_port_role_a = {
                                'admin_speed':admin_speed,
                                'fill_pattern':fill_pattern,
                                'port_id':port_list,
                                'slot_id':1,
                                'vsan_id':vsans.get("Fabric_A")
                            }
                            fc_port_role_b = {
                                'admin_speed':admin_speed,
                                'fill_pattern':fill_pattern,
                                'port_id':port_list,
                                'slot_id':1,
                                'vsan_id':vsans.get("Fabric_B")
                            }
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Do you want to accept the following configuration?')
                            print(f'    admin_speed      = "{admin_speed}"')
                            print(f'    fill_pattern     = "{fill_pattern}"')
                            print(f'    port_list        = "{port_list}"')
                            print(f'    vsan_id_fabric_a = {vsans.get("Fabric_A")}')
                            print(f'    vsan_id_fabric_b = {vsans.get("Fabric_B")}')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            valid_confirm = False
                            while valid_confirm == False:
                                confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                if confirm_port == 'Y' or confirm_port == '':
                                    Fabric_A_port_role_fc.append(fc_port_role_a)
                                    Fabric_B_port_role_fc.append(fc_port_role_b)
                                    for i in port_list:
                                        fc_ports_in_use.append(i)

                                    valid_exit = False
                                    while valid_exit == False:
                                        port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                        if port_exit == 'Y':
                                            port_count += 1
                                            valid_confirm = True
                                            valid_exit = True
                                        elif port_exit == 'N' or port_exit == '':
                                            configure_valid = True
                                            valid = True
                                            valid_confirm = True
                                            valid_exit = True
                                        else:
                                            print(f'\n------------------------------------------------------\n')
                                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                            print(f'\n------------------------------------------------------\n')

                                elif confirm_port == 'N':
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Starting {port_type} Configuration Over.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    valid_confirm = True
                                else:
                                    print(f'\n------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                    print(f'\n------------------------------------------------------\n')

                    elif configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_role_fcoe_uplinks = []
                port_type = 'FCoE Uplink'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure an {port_type}?  Enter "Y" or "N" [N]: ')
                    if configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5-10 - Range of Ports')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'     5-10,20-30 - Ranges and Lists of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [97]: ')
                            else:
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [49]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '97'
                            elif port_list == '':
                                port_list = '49'
                            if re.search(r'(^\d+$|^\d+,{1,48}\d+$|^(\d+\-\d+|\d,){1,48}\d+$)', port_list):
                                original_port_list = port_list
                                ports_expanded = vlan_list_full(port_list)
                                port_list = ports_expanded
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'ethernet_admin_speed.txt'
                                        templateVars["var_description"] = '    Please Select the Admin Speed for the Port:\n'
                                        templateVars["var_type"] = 'Admin Speed'
                                        admin_speed = variable_loop(**templateVars)

                                        # Prompt User for the Admin Speed of the Port
                                        templateVars["multi_select"] = False
                                        templateVars["policy_file"] = 'fec.txt'
                                        templateVars["var_description"] = '    Forward error correction configuration for the port:\n'\
                                            '    - Auto - (Default).  Forward error correction option Auto.\n'\
                                            '    - Cl91 - Forward error correction option cl91\n'\
                                            '    - Cl74 - Forward error correction option cl74.\n'
                                        templateVars["var_type"] = 'FEC'
                                        fec = variable_loop(**templateVars)

                                        # Prompt User for the
                                        policy_list = [
                                            'policies.link_control_policies.link_control_policy'
                                        ]
                                        templateVars["allow_opt_out"] = True
                                        for policy in policy_list:
                                            policy_short = policy.split('.')[2]
                                            templateVars[policy_short],
                                            policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                            templateVars.update(policyData)

                                        port_role = {
                                            'admin_speed':admin_speed,
                                            'fec':fec,
                                            'link_control_policy':templateVars["link_control_policy"],
                                            'port_id':original_port_list,
                                            'slot_id':1
                                        }
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following configuration?')
                                        print(f'    admin_speed         = "{admin_speed}"')
                                        print(f'    fec                 = "{fec}"')
                                        print(f'    link_control_policy = "{templateVars["link_control_policy"]}"')
                                        print(f'    port_list           = "{original_port_list}"')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                port_role_fcoe_uplinks.append(port_role)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure another {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == '' or configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                port_role_servers = []
                port_type = 'Server Ports'
                port_count = 1
                valid = False
                while valid == False:
                    configure_port = input(f'Do you want to configure {port_type}?  Enter "Y" or "N" [Y]: ')
                    if configure_port == '' or configure_port == 'Y':
                        configure_valid = False
                        while configure_valid == False:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  The Port List can be in the format of:')
                            print(f'     5 - Single Port')
                            print(f'     5-10 - Range of Ports')
                            print(f'     5,11,12,13,14,15 - List of Ports')
                            print(f'     5-10,20-30 - Ranges and Lists of Ports')
                            print(f'\n------------------------------------------------------\n')
                            if model == 'UCS-FI-64108':
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [5-36]: ')
                            else:
                                port_list = input(f'Please enter the list of ports you want to add to the {port_type}?  [5-18]: ')
                            if port_list == '' and model == 'UCS-FI-64108':
                                port_list = '5-36'
                            elif port_list == '':
                                port_list = '5-18'
                            if re.search(r'(^\d+$|^\d+,{1,48}\d+$|^(\d+\-\d+|\d,){1,48}\d+$)', port_list):
                                original_port_list = port_list
                                ports_expanded = vlan_list_full(port_list)
                                port_list = ports_expanded
                                port_overlap_count = 0
                                port_overlap = []
                                for x in ports_in_use:
                                    for y in port_list:
                                        if int(x) == int(y):
                                            port_overlap_count += 1
                                            port_overlap.append(x)
                                if port_overlap_count == 0:
                                    if model == 'UCS-FI-64108':
                                        max_port = 108
                                    else:
                                        max_port = 54
                                    if fc_mode == 'Y':
                                        min_port = int(fc_ports[1])
                                    else:
                                        min_port = 1
                                    for port in port_list:
                                        valid_ports = validating_ucs.number_in_range('Port Range', port, min_port, max_port)
                                        if valid_ports == False:
                                            break
                                    if valid_ports == True:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Do you want to accept the following Server Port configuration?')
                                        print(f'    port_list           = "{original_port_list}"')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = False
                                        while valid_confirm == False:
                                            confirm_port = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                                            if confirm_port == 'Y' or confirm_port == '':
                                                server_ports = {'port_list':original_port_list,'slot_id':1}
                                                port_role_servers.append(server_ports)
                                                for i in port_list:
                                                    ports_in_use.append(i)

                                                valid_exit = False
                                                while valid_exit == False:
                                                    port_exit = input(f'Would You like to Configure more {port_type}?  Enter "Y" or "N" [N]: ')
                                                    if port_exit == 'Y':
                                                        port_count += 1
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    elif port_exit == 'N' or port_exit == '':
                                                        configure_valid = True
                                                        valid = True
                                                        valid_confirm = True
                                                        valid_exit = True
                                                    else:
                                                        print(f'\n------------------------------------------------------\n')
                                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                        print(f'\n------------------------------------------------------\n')

                                            elif confirm_port == 'N':
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                print(f'  Starting {port_type} Configuration Over.')
                                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                                valid_confirm = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! The following Ports are already in use: {port_overlap}.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Port Range.  A port Range should be in the format 49-50 for example.')
                                print(f'  The following port range is invalid: "{port_list}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                    elif configure_port == 'N':
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description  = "{templateVars["descr"]}"')
                print(f'    device_model = "{templateVars["device_model"]}"')
                print(f'    name         = "{templateVars["name"]}"')
                if len(port_channel_appliances) > 0:
                    print(f'    port_channel_appliances = [')
                    for item in port_channel_appliances:
                        for k, v in item.items():
                            if k == 'pc_id':
                                print(f'      {v} = ''{')
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed                     = "{v}"')
                            elif k == 'ethernet_network_control_policy':
                                print(f'        ethernet_network_control_policy = "{v}"')
                            elif k == 'ethernet_network_group_policy':
                                print(f'        ethernet_network_group_policy   = "{v}"')
                            elif k == 'interfaces':
                                print(f'        interfaces = [')
                                for i in v:
                                    print('          {')
                                    for x, y in i.items():
                                        print(f'            {x}          = {y}')
                                    print('          }')
                                print(f'        ]')
                            elif k == 'mode':
                                print(f'        mode     = "{v}"')
                            elif k == 'priority':
                                print(f'        priority = "{v}"')
                        print('      }')
                    print(f'    ]')
                if len(port_channel_ethernet_uplinks) > 0:
                    print(f'    port_channel_ethernet_uplinks = [')
                    for item in port_channel_ethernet_uplinks:
                        for k, v in item.items():
                            if k == 'pc_id':
                                print(f'      {v} = ''{')
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed         = "{v}"')
                            elif k == 'flow_control_policy':
                                print(f'        flow_control_policy = "{v}"')
                            elif k == 'interfaces':
                                print(f'        interfaces = [')
                                for i in v:
                                    print('          {')
                                    for x, y in i.items():
                                        print(f'            {x}          = {y}')
                                    print('          }')
                                print(f'        ]')
                            elif k == 'link_aggregation_policy':
                                print(f'        link_aggregation_policy = "{v}"')
                            elif k == 'link_control_policy':
                                print(f'        link_control_policy     = "{v}"')
                        print('      }')
                    print(f'    ]')
                if len(Fabric_A_fc_port_channels) > 0:
                    print(f'    port_channel_fc_uplinks = [')
                    item_count = 0
                    for item in Fabric_A_fc_port_channels:
                        for k, v in item.items():
                            if k == 'pc_id':
                                print(f'      {v} = ''{')
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed  = "{v}"')
                            elif k == 'fill_pattern':
                                print(f'        fill_pattern = "{v}"')
                            elif k == 'interfaces':
                                print(f'        interfaces = [')
                                for i in v:
                                    print('          {')
                                    for x, y in i.items():
                                        print(f'            {x}          = {y}')
                                    print('          }')
                                print(f'        ]')
                            elif k == 'vsan_id':
                                print(f'        vsan_fabric_a = "{v}"')
                                print(f'        vsan_fabric_b = "{Fabric_B_fc_port_channels[item_count].get("vsan_id")}"')
                        print('      }')
                        item_count += 1
                    print(f'    ]')
                if len(port_channel_fcoe_uplinks) > 0:
                    print(f'    port_channel_fcoe_uplinks = [')
                    for item in port_channel_fcoe_uplinks:
                        for k, v in item.items():
                            if k == 'pc_id':
                                print('      {v} = {')
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed = "{v}"')
                            elif k == 'interfaces':
                                print(f'        interfaces = [')
                                for i in v:
                                    print('          {')
                                    for x, y in i.items():
                                        print(f'            {x}          = {y}')
                                    print('          }')
                                print(f'        ]')
                            elif k == 'link_aggregation_policy':
                                print(f'        link_aggregation_policy = "{v}"')
                            elif k == 'link_control_policy':
                                print(f'        link_control_policy     = "{v}"')
                        print('      }')
                    print(f'    ]')
                if len(templateVars["port_modes"]) > 0:
                    print('    port_modes = {')
                    for k, v in templateVars["port_modes"].items():
                        if k == 'custom_mode':
                            print(f'      custom_mode = "{v}"')
                        elif k == 'port_list':
                            print(f'      port_list   = "{v}"')
                        elif k == 'slot_id':
                            print(f'      slot_id     = {v}')
                    print('    }')
                item_count = 0
                if len(port_role_appliances) > 0:
                    print(f'    port_role_appliances = [')
                    for item in port_role_appliances:
                        print(f'      {item_count} = ''{')
                        item_count += 1
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed                     = "{v}"')
                            elif k == 'ethernet_network_control_policy':
                                print(f'        ethernet_network_control_policy = "{v}"')
                            elif k == 'ethernet_network_group_policy':
                                print(f'        ethernet_network_group_policy   = "{v}"')
                            elif k == 'fec':
                                print(f'        fec                             = "{v}"')
                            elif k == 'mode':
                                print(f'        mode                            = "{v}"')
                            elif k == 'port_id':
                                print(f'        port_list                       = "{v}"')
                            elif k == 'priority':
                                print(f'        priority                        = "{v}"')
                            elif k == 'slot_id':
                                print(f'        slot_id                         = 1')
                        print('      }')
                    print(f'    ]')
                item_count = 0
                if len(port_role_ethernet_uplinks) > 0:
                    print(f'    port_role_ethernet_uplinks = [')
                    for item in port_role_ethernet_uplinks:
                        print(f'      {item_count} = ''{')
                        item_count += 1
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed         = "{v}"')
                            elif k == 'fec':
                                print(f'        fec                 = "{v}"')
                            elif k == 'flow_control_policy':
                                print(f'        flow_control_policy = "{v}"')
                            elif k == 'link_control_policy':
                                print(f'        link_control_policy = "{v}"')
                            elif k == 'port_id':
                                print(f'        port_list           = "{v}"')
                            elif k == 'slot_id':
                                print(f'        slot_id             = 1')
                        print('      }')
                    print(f'    ]')
                item_count = 0
                if len(Fabric_A_port_role_fc) > 0:
                    print(f'    port_role_fc_uplinks = [')
                    for item in Fabric_A_port_role_fc:
                        print(f'      {item_count} = ''{')
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed   = "{v}"')
                            elif k == 'fill_pattern':
                                print(f'        fill_pattern  = "{v}"')
                            elif k == 'port_id':
                                print(f'        port_list     = "{v}"')
                            elif k == 'slot_id':
                                print(f'        slot_id       = 1')
                            elif k == 'vsan_id':
                                print(f'        vsan_fabric_a = "{v}"')
                                print(f'        vsan_fabric_b = "{Fabric_B_port_role_fc[item_count].get("vsan_id")}"')
                        print('      }')
                        item_count += 1
                    print(f'    ]')
                item_count = 0
                if len(port_role_fcoe_uplinks) > 0:
                    print(f'    port_role_fcoe_uplinks = [')
                    for item in port_role_fcoe_uplinks:
                        print(f'      {item_count} = ''{')
                        item_count += 1
                        for k, v in item.items():
                            if k == 'admin_speed':
                                print(f'        admin_speed         = "{v}"')
                            elif k == 'fec':
                                print(f'        fec                 = "{v}"')
                            elif k == 'link_control_policy':
                                print(f'        link_control_policy = "{v}"')
                            elif k == 'port_id':
                                print(f'        port_list           = "{v}"')
                            elif k == 'slot_id':
                                print(f'        slot_id             = 1')
                        print('      }')
                    print(f'    ]')
                if len(port_role_servers) > 0:
                    print(f'    port_role_servers = [')
                    for item in port_role_servers:
                        print(f'      {item_count} = ''{')
                        item_count += 1
                        for k, v in item.items():
                            if k == 'port_list':
                                print(f'        port_list           = "{v}"')
                            if k == 'slot_id':
                                print(f'        slot_id             = {v}')
                        print('      }')
                    print(f'    ]')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Do you want to accept the above Port Policy configuration?  Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        templateVars["port_channel_appliances"] = port_channel_appliances
                        templateVars["port_channel_ethernet_uplinks"] = port_channel_ethernet_uplinks
                        templateVars["port_channel_fcoe_uplinks"] = port_channel_fcoe_uplinks
                        templateVars["port_role_appliances"] = port_role_appliances
                        templateVars["port_role_ethernet_uplinks"] = port_role_ethernet_uplinks
                        templateVars["port_role_fcoe_uplinks"] = port_role_fcoe_uplinks
                        templateVars["port_role_servers"] = port_role_servers
                        # templateVars["port_modes"] = [{'custom_mode':'FibreChannel','port_list':fc_ports,'slot_id':1}]

                        original_name = templateVars["name"]
                        templateVars["name"] = '%s_A' % (original_name)
                        templateVars["port_channel_fc_uplinks"] = Fabric_A_fc_port_channels
                        templateVars["port_role_fc_uplinks"] = Fabric_A_port_role_fc

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        templateVars["name"] = '%s_B' % (original_name)
                        templateVars["port_channel_fc_uplinks"] = Fabric_B_fc_port_channels
                        templateVars["port_role_fc_uplinks"] = Fabric_B_port_role_fc

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Power Policy Module
    #========================================
    def power_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'Power Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'power_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure the Power Redundancy Policies for Chassis and Servers.')
            print(f'  For Servers it will configure the Power Restore State.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            loop_count = 1
            policy_loop = False
            while policy_loop == False:

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'system_type.txt'
                templateVars["var_description"] = '   Please Select the Type of System this Power Policy is for.'
                templateVars["var_type"] = 'System Type'
                system_type = variable_loop(**templateVars)

                print(system_type)
                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, system_type)
                else:
                    name = '%s_%s' % (org, system_type)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                if system_type == '9508':
                    valid = False
                    while valid == False:
                        templateVars["allocated_budget"] = input('What is the Power Budget you would like to Apply?\n'
                            'This should be a value between 2800 Watts and 16800 Watts. [5600]: ')
                        if templateVars["allocated_budget"] == '':
                            templateVars["allocated_budget"] = 5600
                        valid = validating_ucs.number_in_range('Chassis Power Budget', templateVars["allocated_budget"], 2800, 16800)
                else:
                    templateVars["allocated_budget"] = 0

                if system_type == 'Server':
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'power_restore.txt'
                    templateVars["var_description"] = '   Sets the Power Restore State of the Server.\n'\
                        '      - AlwaysOff - Set the Power Restore Mode to Off.\n'\
                        '      - AlwaysOn - Set the Power Restore Mode to On.\n'\
                        '      - LastState - Set the Power Restore Mode to LastState.\n'
                    templateVars["var_type"] = 'Power Restore State'
                    templateVars["power_restore_state"] = variable_loop(**templateVars)

                if system_type == '5108':
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'power_5108.txt'
                    templateVars["var_description"] = '    Please Select the Power Redundancy Policy to apply to the system\n'\
                        '      - Grid - Grid Mode requires two power sources. If one source fails, the surviving PSUs connected to the other source provides power to the chassis.\n'\
                        '      - NotRedundant - Power Manager turns on the minimum number of PSUs required to support chassis power requirements. No Redundant PSUs are maintained.\n'\
                        '      - N+1 - Power Manager turns on the minimum number of PSUs required to support chassis power requirements plus one additional PSU for redundancy.\n'
                elif system_type == '9508':
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'power_9508.txt'
                    templateVars["var_description"] = '   Please Select the Power Redundancy Policy to apply to the system\n'\
                        '      - Grid - Grid Mode requires two power sources. If one source fails, the surviving PSUs connected to the other source provides power to the chassis.\n'\
                        '      - NotRedundant - Power Manager turns on the minimum number of PSUs required to support chassis power requirements. No Redundant PSUs are maintained.\n'\
                        '      - N+1 - Power Manager turns on the minimum number of PSUs required to support chassis power requirements plus one additional PSU for redundancy.\n'\
                        '      - N+2 - Power Manager turns on the minimum number of PSUs required to support chassis power requirements plus two additional PSU for redundancy.\n'
                elif system_type == 'Server':
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'power_server.txt'
                    templateVars["var_description"] = '   Please Select the Power Redundancy Policy to apply to the system\n'\
                        '      - Grid - Grid Mode requires two power sources. If one source fails, the surviving PSUs connected to the other source provides power to the chassis.\n'\
                        '      - NotRedundant - Power Manager turns on the minimum number of PSUs required to support chassis power requirements. No Redundant PSUs are maintained.\n'
                templateVars["var_type"] = 'Power Redundancy Mode'
                templateVars["redundancy_mode"] = variable_loop(**templateVars)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                if system_type == '9508':
                    print(f'   allocated_budget    = {templateVars["allocated_budget"]}')
                print(f'   description         = "{templateVars["descr"]}"')
                print(f'   name                = "{templateVars["name"]}"')
                if system_type == 'Server':
                    print(f'   power_restore_state = "{templateVars["power_restore_state"]}"')
                print(f'   redundancy_mode     = "{templateVars["redundancy_mode"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Do you want to accept the above Configuration?  Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_yes(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # SAN Connectivity Policy Module
    #========================================
    def san_connectivity_policies(self, pci_order_consumed):
        name_prefix = self.name_prefix
        name_suffix = 'san'
        org = self.org
        policy_type = 'SAN Connectivity Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'san_connectivity_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  You can Skip this policy if you are not configuring Fibre-Channel.\n')
            print(f'  A {policy_type} will configure vHBA adapters for Server Profiles.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'target_platform.txt'
                    templateVars["var_description"] = '    The platform for which the server profile is applicable. It can either be:\n'
                    templateVars["var_type"] = 'Target Platform'
                    target_platform = variable_loop(**templateVars)
                    templateVars["target_platform"] = target_platform

                    if target_platform == 'FIAttached':
                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'placement_mode.txt'
                        templateVars["var_description"] = '    The most common implementation is custom.\n'\
                            '    The mode used for placement of vHBAs on network adapters. Options are:\n'
                        templateVars["var_type"] = 'vHBA Placement Mode'
                        templateVars["vhba_placement_mode"] = variable_loop(**templateVars)

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'allocation_type.txt'
                        templateVars["var_description"] = '    Allocation method to assign a WWNN address for consumers of the san policy.\n'
                        templateVars["var_type"] = 'WWNN Allocation Type'
                        templateVars["wwnn_allocation_type"] = variable_loop(**templateVars)

                        templateVars["wwnn_pool"] = ''
                        templateVars["wwnn_static"] = ''
                        if templateVars["wwnn_allocation_type"] == 'Pool':
                            policy_list = [
                                'pools.wwnn_pools.wwnn_pool'
                            ]
                            templateVars["allow_opt_out"] = False
                            for policy in policy_list:
                                templateVars["wwnn_pool"],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                templateVars.update(policyData)

                        else:
                            valid = False
                            while valid == False:
                                templateVars["wwnn_static"] = input(f'What is the Static WWNN you would like to assign to this SAN Policy?  ')
                                if not templateVars["wwnn_static"] == '':
                                    valid = validating_ucs.wwxn_address('WWNN Static', templateVars["wwnn_static"])

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'   BEGINNING vHBA Creation Process')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    fabrics = ['A', 'B']
                    templateVars["vhbas"] = []
                    inner_loop_count = 1
                    vhba_loop = False
                    while vhba_loop == False:
                        temp_policy_name = templateVars["name"]
                        templateVars["name"] = 'the vHBAs'
                        policy_list = [
                            'policies.fibre_channel_adapter_policies.fibre_channel_adapter_policy'
                            'policies.fibre_channel_qos_policies.fibre_channel_qos_policy'
                        ]
                        templateVars["allow_opt_out"] = False
                        for policy in policy_list:
                            policy_short = policy.split('.')[2]
                            templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                            templateVars.update(policyData)

                        for x in fabrics:
                            templateVars["name"] = f'the vHBA on Fabric {x}'
                            policy_list = [
                                'policies.fibre_channel_network_policies.fibre_channel_network_policy'
                            ]
                            templateVars["allow_opt_out"] = False
                            for policy in policy_list:
                                policy_short = item.split('.')[2]
                                templateVars[f"{policy_short}_{x}"],
                                policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                templateVars.update(policyData)

                        templateVars["name"] = temp_policy_name

                        for x in fabrics:
                            valid = False
                            while valid == False:
                                templateVars[f'name_{x}'] = input(f'What is the name for Fabric {x} vHBA?  [HBA-{x}]: ')
                                if templateVars[f'name_{x}'] == '':
                                    templateVars[f'name_{x}'] = 'HBA-%s' % (x)
                                valid = validating_ucs.vname('vNIC Name', templateVars[f'name_{x}'])

                        valid = False
                        while valid == False:
                            question = input(f'\nNote: Persistent LUN Binding Enables retention of LUN ID associations in memory until they are'\
                                ' manually cleared.\n\n'\
                                'Do you want to Enable Persistent LUN Bindings?    Enter "Y" or "N" [N]: ')
                            if question == '' or question == 'N':
                                templateVars["persistent_lun_bindings"] = False
                                valid = True
                            elif question == 'Y':
                                templateVars["persistent_lun_bindings"] = True
                                valid = True
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'    The PCI Link used as transport for the virtual interface. All VIC adapters have a')
                        print(f'    single PCI link except VIC 1385 which has two.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        for x in fabrics:
                            valid = False
                            while valid == False:
                                question = input(f'What is the PCI Link you want to Assign to Fabric {x}?  Range is 0-1.  [0]: ')
                                if question == '' or int(question) == 0:
                                    templateVars[f"pci_link_{x}"] = 0
                                    valid = True
                                elif int(question) == 1:
                                    templateVars[f"pci_link_{x}"] = 1
                                    valid = True
                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please enter 0 or 1.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'    PCI Order establishes The order in which the virtual interface is brought up. The order ')
                        print(f'    assigned to an interface should be unique for all the Ethernet and Fibre-Channel ')
                        print(f'    interfaces on each PCI link on a VIC adapter. The maximum value of PCI order is limited ')
                        print(f'    by the number of virtual interfaces (Ethernet and Fibre-Channel) on each PCI link on a ')
                        print(f'    VIC adapter. All VIC adapters have a single PCI link except VIC 1385 which has two.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        pci_order_0 = 0
                        pci_order_1 = 0
                        for x in fabrics:
                            for item in pci_order_consumed:
                                for k, v in item.items():
                                    if int(k) == 0:
                                        for i in v:
                                            pci_order_0 = i
                                    else:
                                        for i in v:
                                            pci_order_1 = i
                            valid = False
                            while valid == False:
                                if templateVars[f'pci_link_{x}'] == 0:
                                    pci_order = (int(pci_order_0) + 1)
                                elif templateVars[f'pci_link_{x}'] == 1:
                                    pci_order = (int(pci_order_1) + 1)
                                question = input(f'What is the PCI Order you want to Assign to Fabric {x}?  [{pci_order}]: ')
                                if question == '':
                                    templateVars[f"pci_order_{x}"] = pci_order
                                duplicate = 0
                                for item in pci_order_consumed:
                                    for k, v in item.items():
                                        if templateVars[f'pci_link_{x}'] == 0 and int(k) == 0:
                                            for i in v:
                                                if int(i) == int(pci_order):
                                                    duplicate += 1
                                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                                    print(f'  Error!! PCI Order "{pci_order}" is already in use.  Please use an alternate.')
                                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                        elif templateVars[f'pci_link_{x}'] == 1 and int(k) == 1:
                                            for i in v:
                                                if int(i) == int(pci_order):
                                                    duplicate += 1
                                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                                    print(f'  Error!! PCI Order "{pci_order}" is already in use.  Please use an alternate.')
                                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                if duplicate == 0:
                                    if templateVars[f'pci_link_{x}'] == 0:
                                        pci_order_consumed[0][0].append(pci_order)
                                    elif templateVars[f'pci_link_{x}'] == 1:
                                        pci_order_consumed[1][1].append(pci_order)
                                    valid = True

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'slot_id.txt'
                        templateVars["var_description"] = '  PCIe Slot where the VIC adapter is installed. Supported values are (1-15) and MLOM.\n\n'
                        templateVars["var_type"] = 'Slot ID'
                        templateVars["slot_id"] = variable_loop(**templateVars)

                        if not target_platform == 'FIAttached':
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'    The Uplink Port is the Adapter port on which the virtual interface will be created.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            for x in fabrics:
                                valid = False
                                while valid == False:
                                    question = input(f'What is the Uplink Port you want to Assign to Fabric {x}?  Range is 0-3.  [0]: ')
                                    if question == '':
                                        templateVars[f"uplink_port_{x}"] = 0
                                    if re.fullmatch(r'^[0-3]', str(question)):
                                        templateVars[f"uplink_port_{x}"] = question
                                        valid = validating_ucs.number_in_range(f'Fabric {x} PCI Uplink', templateVars[f"uplink_port_{x}"], 0, 3)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter 0 or 1.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'vhba_type.txt'
                        templateVars["var_description"] = '    vhba_type - VHBA Type for the vHBA Policy.\n'\
                            '    - fc-initiator (Default) - The default value set for vHBA Type Configuration. \n'\
                            '         Fc-initiator specifies vHBA as a consumer of storage. Enables SCSI commands to\n'\
                            '         transfer data and status information between host and target storage systems.\n'\
                            '    - fc-nvme-initiator - Fc-nvme-initiator specifies vHBA as a consumer of storage. \n'\
                            '         Enables NVMe-based message commands to transfer data and status information \n'\
                            '         between host and target storage systems.\n'\
                            '    - fc-nvme-target - Fc-nvme-target specifies vHBA as a provider of storage volumes to\n'\
                            '         initiators.  Enables NVMe-based message commands to transfer data and status \n'\
                            '         information between host and target storage systems.  Currently tech-preview, \n'\
                            '         only enabled with an asynchronous driver.\n'\
                            '    - fc-target - Fc-target specifies vHBA as a provider of storage volumes to initiators. \n'\
                            '         Enables SCSI commands to transfer data and status information between host and \n'\
                            '         target storage systems.  fc-target is enabled only with an asynchronous driver.\n\n'
                        templateVars["var_type"] = 'vHBA Type'
                        templateVars["vhba_type"] = variable_loop(**templateVars)

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'allocation_type.txt'
                        templateVars["var_description"] = '    Type of allocation to assign a WWPN address to each vHBA for this SAN policy.\n'
                        templateVars["var_type"] = 'WWPN Allocation Type'
                        templateVars["wwpn_allocation_type"] = variable_loop(**templateVars)

                        if target_platform == 'FIAttached':
                            templateVars[f'wwpn_pool_A'] = ''
                            templateVars[f'wwpn_pool_B'] = ''
                            templateVars[f'wwpn_static_A'] = ''
                            templateVars[f'wwpn_static_B'] = ''
                            if templateVars["wwpn_allocation_type"] == 'Pool':
                                policy_list = [
                                    'pools.wwpn_pools.wwpn_pool'
                                ]
                                templateVars["allow_opt_out"] = False
                                for x in fabrics:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Select WWPN Pool for Fabric {x}:')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    for policy in policy_list:
                                        policy_short = policy.split('.')[2]
                                        templateVars[f'{policy_short}_{x}'],
                                        policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                        templateVars.update(policyData)

                            else:
                                valid = False
                                while valid == False:
                                    for x in fabrics:
                                        templateVars["wwpn_static"] = input(f'What is the Static WWPN you would like to assign to Fabric {x}?  ')
                                    if not templateVars["wwpn_static"] == '':
                                        templateVars[f"wwpn_static_{x}"]
                                        valid = validating_ucs.wwxn_address(f'Fabric {x} WWPN Static', templateVars["wwpn_static"])

                        if target_platform == 'FIAttached':
                            vhba_fabric_a = {
                                'fibre_channel_adapter_policy':templateVars["fibre_channel_adapter_policy"],
                                'fibre_channel_network_policy':templateVars["fibre_channel_network_policy_A"],
                                'fibre_channel_qos_policy':templateVars["fibre_channel_qos_policy"],
                                'name':templateVars["name_A"],
                                'persistent_lun_bindings':templateVars["persistent_lun_bindings"],
                                'pci_link':templateVars["pci_link_A"],
                                'pci_order':templateVars["pci_order_A"],
                                'slot_id':templateVars["slot_id"],
                                'switch_id':'A',
                                'vhba_type':templateVars["vhba_type"],
                                'wwpn_allocation_type':templateVars["wwpn_allocation_type"],
                                'wwpn_pool':templateVars["wwpn_pool_A"],
                                'wwpn_static':templateVars["wwpn_static_A"],
                            }
                            vhba_fabric_b = {
                                'fibre_channel_adapter_policy':templateVars["fibre_channel_adapter_policy"],
                                'fibre_channel_network_policy':templateVars["fibre_channel_network_policy_B"],
                                'fibre_channel_qos_policy':templateVars["fibre_channel_qos_policy"],
                                'name':templateVars["name_B"],
                                'persistent_lun_bindings':templateVars["persistent_lun_bindings"],
                                'pci_link':templateVars["pci_link_B"],
                                'pci_order':templateVars["pci_order_B"],
                                'slot_id':templateVars["slot_id"],
                                'switch_id':'B',
                                'vhba_type':templateVars["vhba_type"],
                            }
                        else:
                            vhba_fabric_a = {
                                'fibre_channel_adapter_policy':templateVars["fibre_channel_adapter_policy"],
                                'fibre_channel_network_policy':templateVars["fibre_channel_network_policy_A"],
                                'fibre_channel_qos_policy':templateVars["fibre_channel_qos_policy"],
                                'name':templateVars["name_A"],
                                'persistent_lun_bindings':templateVars["persistent_lun_bindings"],
                                'pci_link':templateVars["pci_link_A"],
                                'pci_order':templateVars["pci_order_A"],
                                'slot_id':templateVars["slot_id"],
                                'uplink_port':templateVars["uplink_port_A"],
                                'vhba_type':templateVars["vhba_type"],
                            }
                            vhba_fabric_b = {
                                'fibre_channel_adapter_policy':templateVars["fibre_channel_adapter_policy"],
                                'fibre_channel_network_policy':templateVars["fibre_channel_network_policy_B"],
                                'fibre_channel_qos_policy':templateVars["fibre_channel_qos_policy"],
                                'name':templateVars["name_B"],
                                'persistent_lun_bindings':templateVars["persistent_lun_bindings"],
                                'pci_link':templateVars["pci_link_B"],
                                'pci_order':templateVars["pci_order_B"],
                                'slot_id':templateVars["slot_id"],
                                'uplink_port':templateVars["uplink_port_B"],
                                'vhba_type':templateVars["vhba_type"],
                                'wwpn_allocation_type':templateVars["wwpn_allocation_type"],
                                'wwpn_pool':templateVars["wwpn_pool_B"],
                                'wwpn_static':templateVars["wwpn_static_B"],
                            }
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'Fabric A:')
                        print(f'   fibre_channel_adapter_policy = "{templateVars["fibre_channel_adapter_policy"]}"')
                        print(f'   fibre_channel_network_policy = "{templateVars["fibre_channel_network_policy_A"]}"')
                        print(f'   fibre_channel_qos_policy     = "{templateVars["fibre_channel_qos_policy"]}"')
                        print(f'   name                         = "{templateVars["name_A"]}"')
                        print(f'   persistent_lun_bindings      = {templateVars["persistent_lun_bindings"]}')
                        print(f'   placement_pci_link           = {templateVars["pci_link_A"]}')
                        print(f'   placement_pci_order          = {templateVars["pci_order_A"]}')
                        print(f'   placement_slot_id            = "{templateVars["slot_id"]}"')
                        if target_platform == 'FIAttached':
                            print(f'   placement_switch_id          = "A"')
                        else:
                            print(f'   placement_uplink_port        = "{templateVars["uplink_port_A"]}"')
                        print(f'   vhba_type                    = "{templateVars["vhba_type"]}"')
                        print(f'   wwpn_allocation_type         = "{templateVars["wwpn_allocation_type"]}"')
                        if templateVars["wwpn_allocation_type"] == 'Pool':
                            print(f'   wwpn_pool                    = "{templateVars["wwpn_pool_A"]}"')
                        else:
                            print(f'   wwpn_static_address          = "{templateVars["wwpn_static_A"]}"')
                        print(f'Fabric B:')
                        print(f'   fibre_channel_adapter_policy = "{templateVars["fibre_channel_adapter_policy"]}"')
                        print(f'   fibre_channel_network_policy = "{templateVars["fibre_channel_network_policy_B"]}"')
                        print(f'   fibre_channel_qos_policy     = "{templateVars["fibre_channel_qos_policy"]}"')
                        print(f'   name                         = "{templateVars["name_B"]}"')
                        print(f'   persistent_lun_bindings      = {templateVars["persistent_lun_bindings"]}')
                        print(f'   placement_pci_link           = {templateVars["pci_link_B"]}')
                        print(f'   placement_pci_order          = {templateVars["pci_order_B"]}')
                        print(f'   placement_slot_id            = "{templateVars["slot_id"]}"')
                        if target_platform == 'FIAttached':
                            print(f'   placement_switch_id          = "B"')
                        else:
                            print(f'   placement_uplink_port        = "{templateVars["uplink_port_B"]}"')
                        print(f'   vhba_type                    = "{templateVars["vhba_type"]}"')
                        if target_platform == 'FIAttached':
                            print(f'   wwpn_allocation_type         = "{templateVars["wwpn_allocation_type"]}"')
                            if templateVars["wwpn_allocation_type"] == 'Pool':
                                print(f'   wwpn_pool                    = "{templateVars["wwpn_pool_B"]}"')
                            else:
                                print(f'   wwpn_static_address          = "{templateVars["wwpn_static_B"]}"')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        valid_confirm = False
                        while valid_confirm == False:
                            confirm_v = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                            if confirm_v == 'Y' or confirm_v == '':
                                templateVars["vhbas"].append(vhba_fabric_a)
                                templateVars["vhbas"].append(vhba_fabric_b)
                                valid_exit = False
                                while valid_exit == False:
                                    loop_exit = input(f'Would You like to Configure another set of vHBAs?  Enter "Y" or "N" [N]: ')
                                    if loop_exit == 'Y':
                                        inner_loop_count += 1
                                        valid_confirm = True
                                        valid_exit = True
                                    elif loop_exit == 'N' or loop_exit == '':
                                        vhba_loop = True
                                        valid_confirm = True
                                        valid_exit = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                            elif confirm_v == 'N':
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Starting Remote Host Configuration Over.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = True
                            else:
                                print(f'\n------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n------------------------------------------------------\n')


                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    description          = "{templateVars["descr"]}"')
                    print(f'    name                 = "{templateVars["name"]}"')
                    print(f'    target_platform      = "{target_platform}"')
                    if target_platform == 'FIAttached':
                        print(f'    vhba_placement_mode  = "{templateVars["vhba_placement_mode"]}"')
                        print(f'    wwnn_allocation_type = "{templateVars["wwnn_allocation_type"]}"')
                        print(f'    wwnn_pool            = "{templateVars["wwnn_pool"]}"')
                        print(f'    wwnn_static          = "{templateVars["wwnn_static"]}"')
                    if len(templateVars["vhbas"]) > 0:
                        print(f'    vhbas = ''[')
                        for item in templateVars["vhbas"]:
                            print(f'      ''{')
                            for k, v in item.items():
                                if k == 'fibre_channel_adapter_policy':
                                    print(f'        fibre_channel_adapter_policy = "{v}"')
                                elif k == 'fibre_channel_network_policy':
                                    print(f'        fibre_channel_network_policy = "{v}"')
                                elif k == 'fibre_channel_qos_policy':
                                    print(f'        fibre_channel_qos_policy     = "{v}"')
                                elif k == 'name':
                                    print(f'        name                         = {v}')
                                elif k == 'persistent_lun_bindings':
                                    print(f'        persistent_lun_bindings      = {v}')
                                elif k == 'pci_link':
                                    print(f'        placement_pci_link           = {v}')
                                elif k == 'pci_link':
                                    print(f'        placement_pci_order          = {v}')
                                elif k == 'placement_slot_id':
                                    print(f'        placement_slot_id            = "{v}"')
                                elif k == 'switch_id':
                                    print(f'        placement_switch_id          = "{v}"')
                                elif k == 'uplink_port':
                                    print(f'        placement_uplink_port        = "{v}"')
                                elif k == 'vhba_type':
                                    print(f'        vhba_type                    = "{v}"')
                                elif k == 'wwpn_allocation_type':
                                    print(f'        wwpn_allocation_type         = "{v}"')
                                elif k == 'wwpn_pool':
                                    print(f'        wwpn_pool                    = "{v}"')
                                elif k == 'wwpn_static':
                                    print(f'        wwpn_static                  = "{v}"')
                            print(f'      ''}')
                        print(f'    '']')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # SD Card Policy Module
    #========================================
    def sd_card_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'sdcard'
        org = self.org
        policy_type = 'SD Card Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'sd_card_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["priority"] = 'auto'
                    templateVars["receive"] = 'Disabled'
                    templateVars["send"] = 'Disabled'

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Serial over LAN Policy Module
    #========================================
    def serial_over_lan_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'sol'
        org = self.org
        policy_type = 'Serial over LAN Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'serial_over_lan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure the Server to allow access to the Communications Port over')
            print(f'  Ethernet.  Settings include:')
            print(f'   - Baud Rate')
            print(f'   - COM Port')
            print(f'   - SSH Port\n')
            print(f'  This Policy is not required to standup a server but is a good practice for day 2 support.')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["enabled"] = True

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'baud_rate.txt'
                    templateVars["var_description"] = '    Please Select the Baud Rate for this Policy.\n'\
                        '    - 115200 - Recommended for best throughput\n'
                    templateVars["var_type"] = 'Baude Rate'
                    templateVars["baud_rate"] = variable_loop(**templateVars)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'com_port.txt'
                    templateVars["var_description"] = '    Please Select the COM Port for this Policy.\n'
                    templateVars["var_type"] = 'COM Port'
                    templateVars["com_port"] = variable_loop(**templateVars)

                    valid = False
                    while valid == False:
                        templateVars["ssh_port"] = input('What is the SSH Port you would like to assign?\n'
                            'This should be a value between 1024-65535. [2400]: ')
                        if templateVars["ssh_port"] == '':
                            templateVars["ssh_port"] = 2400
                        valid = validating_ucs.number_in_range('SSH Port', templateVars["ssh_port"], 1024, 65535)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'   baud_rate   = "{templateVars["baud_rate"]}"')
                    print(f'   com_port    = "{templateVars["com_port"]}"')
                    print(f'   description = "{templateVars["descr"]}"')
                    print(f'   enabled     = "{templateVars["enabled"]}"')
                    print(f'   name        = "{templateVars["name"]}"')
                    print(f'   ssh_port    = "{templateVars["ssh_port"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # SMTP Policy Module
    #========================================
    def smtp_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'smtp'
        org = self.org
        policy_type = 'SMTP Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'smtp_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} sends server faults as email alerts to the configured SMTP server.')
            print(f'  You can specify the preferred settings for outgoing communication and select the fault ')
            print(f'  severity level to report and the mail recipients.\n\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["enable_smtp"] = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  IP address or hostname of the SMTP server. The SMTP server is used by the managed device ')
                    print(f'  to send email notifications.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["smtp_server_address"] = input('What is the SMTP Server Address? ')
                        if re.search(r'^[a-zA-Z0-9]:', templateVars["smtp_server_address"]):
                            valid = validating_ucs.ip_address('SMTP Server Address', templateVars["smtp_server_address"])
                        if re.search(r'[a-zA-Z]', templateVars["smtp_server_address"]):
                            valid = validating_ucs.dns_name('SMTP Server Address', templateVars["smtp_server_address"])
                        elif re.search (r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'):
                            valid = validating_ucs.ip_address('SMTP Server Address', templateVars["smtp_server_address"])
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  "{templateVars["smtp_server_address"]}" is not a valid address.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Port number used by the SMTP server for outgoing SMTP communication.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["smtp_port"] = input('What is the SMTP Port?  [25]: ')
                        if templateVars["smtp_port"] == '':
                            templateVars["smtp_port"] = 25
                        if re.search(r'[\d]+', str(templateVars["smtp_port"])):
                            valid = validating_ucs.number_in_range('SMTP Port', templateVars["smtp_port"], 1, 65535)
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  "{templateVars["smtp_port"]}" is not a valid port.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'smtp_severity.txt'
                    templateVars["var_description"] = '   Minimum fault severity level to receive email notifications. Email notifications\n'\
                        '   are sent for all faults whose severity is equal to or greater than the chosen level.\n'\
                        '   Default is Critical\n'
                    templateVars["var_type"] = 'Minimum Severity'
                    templateVars["minimum_severity"] = variable_loop(**templateVars)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  The email address entered here will be displayed as the from address (mail received from ')
                    print(f'  address) of all the SMTP mail alerts that are received. If not configured, the hostname ')
                    print(f'  of the server is used in the from address field.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["smtp_alert_sender_address"] = input(f'What is the SMTP Alert Sender Address?  '\
                            '[press enter to use server hostname]: ')
                        if templateVars["smtp_alert_sender_address"] == '':
                            templateVars["smtp_alert_sender_address"] = ''
                            valid = True
                        else:
                            valid = validating_ucs.email('SMTP Alert Sender Address', templateVars["smtp_alert_sender_address"])

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  List of email addresses that will receive notifications for faults.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    templateVars["mail_alert_recipients"] = []
                    valid = False
                    while valid == False:
                        mail_recipient = input(f'What is address you would like to send these notifications to?  ')
                        valid_email = validating_ucs.email('Mail Alert Recipient', mail_recipient)
                        if valid_email == True:
                            templateVars["mail_alert_recipients"].append(mail_recipient)
                            valid_answer = False
                            while valid_answer == False:
                                add_another = input(f'Would you like to add another E-mail?  Enter "Y" or "N" [N]: ')
                                if add_another == '' or add_another == 'N':
                                    valid = True
                                    valid_answer = True
                                elif add_another == 'Y':
                                    valid_answer = True
                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'    description               = "{templateVars["descr"]}"')
                    print(f'    enable_smtp                   = {templateVars["enable_smtp"]}')
                    print(f'    mail_alert_recipients     = [')
                    for x in templateVars["mail_alert_recipients"]:
                        print(f'      "{x}",')
                    print(f'    ]')
                    print(f'    minimum_severity          = "{templateVars["minimum_severity"]}"')
                    print(f'    name                      = "{templateVars["name"]}"')
                    print(f'    smtp_alert_sender_address = "{templateVars["smtp_alert_sender_address"]}"')
                    print(f'    smtp_port                 = {templateVars["smtp_port"]}')
                    print(f'    smtp_server_address       = "{templateVars["smtp_server_address"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # SNMP Policy Module
    #========================================
    def snmp_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'snmp'
        org = self.org
        policy_type = 'SNMP Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'snmp_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure chassis, domains, and servers with SNMP parameters.')
            print(f'  This Policy is not required to standup a server but is a good practice for day 2 support.')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 1
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["enabled"] = True

                    valid = False
                    while valid == False:
                        templateVars["port"] = input(f'Note: The following Ports cannot be chosen: [22, 23, 80, 123, 389, 443, 623, 636, 2068, 3268, 3269]\n'\
                            'Enter the Port to Assign to this SNMP Policy.  Valid Range is 1-65535.  [161]: ')
                        if templateVars["port"] == '':
                            templateVars["port"] = 161
                        if re.search(r'[0-9]{1,4}', str(templateVars["port"])):
                            valid = validating_ucs.snmp_port('SNMP Port', templateVars["port"], 1, 65535)
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Invalid Entry!  Please Enter a valid Port in the range of 1-65535.')
                            print(f'  Excluding [22, 23, 80, 123, 389, 443, 623, 636, 2068, 3268, 3269].')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        templateVars["system_contact"] = input(f'Note: Enter a string up to 64 characters, such as an email address or a name and telephone number.\n'\
                            'What is the Contact person responsible for the SNMP implementation?  [UCS Admins]: ')
                        if templateVars["system_contact"] == '':
                            templateVars["system_contact"] = 'UCS Admins'
                        valid = validating_ucs.string_length('System Contact', templateVars["system_contact"], 1, 64)

                    valid = False
                    while valid == False:
                        templateVars["system_location"] = input(f'What is the Location of the host on which the SNMP agent (server) runs?  [Data Center]: ')
                        if templateVars["system_location"] == '':
                            templateVars["system_location"] = 'Data Center'
                        valid = validating_ucs.string_length('System Location', templateVars["system_location"], 1, 64)

                    templateVars["access_community_string"] = ''
                    valid = False
                    while valid == False:
                        question = input(f'Would you like to configure an SNMP Access Community String?  Enter "Y" or "N" [N]: ')
                        if question == 'Y':
                            input_valid = False
                            while input_valid == False:
                                input_string = getpass.getpass(f'What is your SNMP Access Community String? ')
                                if not input_string == '':
                                    input_valid = validating_ucs.snmp_string('SNMP Access Community String', input_string)
                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please Re-enter the SNMP Access Community String.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                            templateVars["access_community_string"] = loop_count
                            TF_VAR = 'TF_VAR_access_community_string_%s' % (loop_count)
                            os.environ[TF_VAR] = '%s' % (input_string)
                            valid = True
                        elif question == '' or question == 'N':
                            valid = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'snmp_community_access.txt'
                    templateVars["var_description"] = '    Controls access to the information in the inventory tables. Applicable only for SNMPv1 and SNMPv2c.\n'\
                        '    - Disabled - (Defualt) - Blocks access to the information in the inventory tables.\n'\
                        '    - Full - Full access to read the information in the inventory tables.\n'\
                        '    - Limited - Partial access to read the information in the inventory tables.\n'
                    templateVars["var_type"] = 'SNMP Community Access'
                    templateVars["community_access"] = variable_loop(**templateVars)

                    templateVars["trap_community_string"] = ''
                    valid = False
                    while valid == False:
                        question = input(f'Would you like to configure an SNMP Trap Community String?  Enter "Y" or "N" [N]: ')
                        if question == 'Y':
                            input_valid = False
                            while input_valid == False:
                                input_string = getpass.getpass(f'What is your SNMP Trap Community String? ')
                                if not input_string == '':
                                    input_valid = validating_ucs.snmp_string('SNMP Trap Community String', input_string)
                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please Re-enter the SNMP Trap Community String.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                            templateVars["trap_community_string"] = loop_count
                            TF_VAR = 'TF_VAR_snmp_trap_community_%s' % (loop_count)
                            os.environ[TF_VAR] = '%s' % (input_string)
                            valid = True
                        elif question == '' or question == 'N':
                            valid = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    templateVars["engine_input_id"] = ''
                    valid = False
                    while valid == False:
                        question = input(f'Note: By default this is derived from the BMC serial number.\n'\
                            'Would you like to configure a Unique string to identify the device for administration purpose?  Enter "Y" or "N" [N]: ')
                        if question == 'Y':
                            input_valid = False
                            while input_valid == False:
                                input_string = input(f'What is the SNMP Engine Input ID? ')
                                if not input_string == '':
                                    input_valid = validating_ucs.string_length('SNMP Engine Input ID', input_string, 1, 27)
                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Error!! Invalid Value.  Please Re-enter the SNMP Engine Input ID.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                            templateVars["snmp_engine_input_id"] = input_string
                            valid = True
                        elif question == '' or question == 'N':
                            valid = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    templateVars["users"] = []
                    inner_loop_count = 1
                    snmp_loop = False
                    while snmp_loop == False:
                        question = input(f'Would you like to configure an SNMPv3 User?  Enter "Y" or "N" [Y]: ')
                        if question == '' or question == 'Y':
                            valid_users = False
                            while valid_users == False:
                                valid = False
                                while valid == False:
                                    snmp_user = input(f'What is your SNMPv3 username? ')
                                    if not snmp_user == '':
                                        valid = validating_ucs.snmp_string('SNMPv3 User', snmp_user)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please Re-enter the SNMPv3 Username.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                templateVars["multi_select"] = False
                                templateVars["policy_file"] = 'snmp_privacy_type.txt'
                                templateVars["var_description"] = '    Security mechanism used for communication between agent and manager:\n'\
                                    '    - AuthNoPriv - The user requires an authorization password but not a privacy password.\n'\
                                    '    - AuthPriv - (Default) - The user requires both an authorization password and a privacy\n'\
                                    '               password.\n'
                                templateVars["var_type"] = 'SNMP Privacy Level'
                                security_level = variable_loop(**templateVars)

                                if security_level == 'AuthNoPriv' or security_level == 'AuthPriv':
                                    templateVars["multi_select"] = False
                                    templateVars["policy_file"] = 'snmp_authorization_protocol.txt'
                                    templateVars["var_description"] = '    Authorization protocol for authenticating the user.  Currently Options are:\n'\
                                        '    - MD5\n'\
                                        '    - SHA - (Default)\n'
                                    templateVars["var_type"] = 'SNMP Authorization Protocol'
                                    auth_type = variable_loop(**templateVars)

                                if security_level == 'AuthNoPriv' or security_level == 'AuthPriv':
                                    valid = False
                                    while valid == False:
                                        auth_password = getpass.getpass(f'What is the authorization password for {snmp_user}? ')
                                        if not auth_password == '':
                                            valid = validating_ucs.snmp_string('SNMPv3 Authorization Password', auth_password)
                                        else:
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                            print(f'  Error!! Invalid Value.  Please Re-enter the SNMPv3 Username.')
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                    TF_VAR = 'TF_VAR_snmp_auth_password_%s' % (inner_loop_count)
                                    os.environ[TF_VAR] = '%s' % (auth_password)
                                    auth_password = inner_loop_count

                                if security_level == 'AuthPriv':
                                    templateVars["multi_select"] = False
                                    templateVars["policy_file"] = 'snmp_privacy_protocol.txt'
                                    templateVars["var_description"] = '    Privacy protocol for the user.  Options are:\n'\
                                        '    - AES - (Default)\n'\
                                        '    - DES\n'
                                    templateVars["var_type"] = 'SNMP Privacy Protocol'
                                    privacy_type = variable_loop(**templateVars)

                                if security_level == 'AuthPriv':
                                    valid = False
                                    while valid == False:
                                        privacy_password = getpass.getpass(f'What is the privacy password for {snmp_user}? ')
                                        if not privacy_password == '':
                                            valid = validating_ucs.snmp_string('SNMPv3 Privacy Password', privacy_password)
                                        else:
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                            print(f'  Error!! Invalid Value.  Please Re-enter the SNMPv3 Username.')
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                    TF_VAR = 'TF_VAR_snmp_privacy_password_%s' % (inner_loop_count)
                                    os.environ[TF_VAR] = '%s' % (privacy_password)
                                    privacy_password = inner_loop_count

                                if security_level == 'AuthPriv':
                                    snmp_userx = {
                                        'auth_password':inner_loop_count,
                                        'auth_type':auth_type,
                                        'name':snmp_user,
                                        'privacy_password':inner_loop_count,
                                        'privacy_type':privacy_type,
                                        'security_level':security_level
                                    }
                                elif security_level == 'AuthNoPriv':
                                    snmp_userx = {
                                        'auth_password':inner_loop_count,
                                        'auth_type':auth_type,
                                        'name':snmp_user,
                                        'security_level':security_level
                                    }

                                # for k, v in os.environ.items():
                                #     print(f'key is {k}, and value is {v}')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'   auth_password    = "Sensitive"')
                                print(f'   auth_type        = "{auth_type}"')
                                if security_level == 'AuthPriv':
                                    print(f'   privacy_password = "Sensitive"')
                                    print(f'   privacy_type     = "{privacy_type}"')
                                print(f'   security_level   = "{security_level}"')
                                print(f'   snmp_user        = "{snmp_user}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = False
                                while valid_confirm == False:
                                    confirm_v = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                                    if confirm_v == 'Y' or confirm_v == '':
                                        templateVars["users"].append(snmp_userx)
                                        valid_exit = False
                                        while valid_exit == False:
                                            loop_exit = input(f'Would You like to Configure another SNMP User?  Enter "Y" or "N" [N]: ')
                                            if loop_exit == 'Y':
                                                inner_loop_count += 1
                                                valid_confirm = True
                                                valid_exit = True
                                            elif loop_exit == 'N' or loop_exit == '':
                                                snmp_loop = True
                                                valid_confirm = True
                                                valid_exit = True
                                                valid_users = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                    elif confirm_v == 'N':
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Starting Remote Host Configuration Over.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                        elif question == 'N':
                            snmp_loop = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')


                    snmp_user_list = []
                    if len(templateVars["users"]):
                        for item in templateVars["users"]:
                            for k, v in item.items():
                                if k == 'name':
                                    snmp_user_list.append(v)

                    templateVars["trap_destinations"] = []
                    inner_loop_count = 1
                    snmp_loop = False
                    while snmp_loop == False:
                        question = input(f'Would you like to configure SNMP Trap Destionations?  Enter "Y" or "N" [Y]: ')
                        if question == '' or question == 'Y':
                            valid_traps = False
                            while valid_traps == False:
                                if len(snmp_user_list) == 0:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  There are no valid SNMP Users so Trap Destinations can only be set to SNMPv2.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    snmp_version = 'V2'
                                else:
                                    templateVars["multi_select"] = False
                                    templateVars["policy_file"] = 'snmp_version.txt'
                                    templateVars["var_description"] = '    What Version of SNMP will be used for this Trap Destination?\n'\
                                        '    - V2 - SNMPv2c.\n'\
                                        '    - V3 - (Defualt - SNMPv3\n'
                                    templateVars["var_type"] = 'SNMP Version'
                                    snmp_version = variable_loop(**templateVars)

                                if snmp_version == 'V2':
                                    valid = False
                                    while valid == False:
                                        community_string = getpass.getpass(f'What is the Community String for the Destination? ')
                                        if not community_string == '':
                                            valid = validating_ucs.snmp_string('SNMP Community String', community_string)
                                        else:
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                            print(f'  Error!! Invalid Value.  Please Re-enter the SNMP Community String.')
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                    TF_VAR = 'TF_VAR_snmp_community_string_%s' % (inner_loop_count)
                                    os.environ[TF_VAR] = '%s' % (community_string)
                                    community_string = inner_loop_count

                                if snmp_version == 'V3':
                                    templateVars["multi_select"] = False
                                    templateVars["var_description"] = '    Please Select the SNMP User to assign to this Destination:\n'
                                    templateVars["var_type"] = 'SNMP User'
                                    snmp_user = vars_from_list(snmp_user_list, **templateVars)
                                    snmp_user = snmp_user[0]

                                if snmp_version == 'V2':
                                    templateVars["multi_select"] = False
                                    templateVars["policy_file"] = 'snmp_trap_type.txt'
                                    templateVars["var_description"] = '    Type of trap which decides whether to receive a notification when a trap is received at the destination.\n'\
                                        '    - Inform - Receive notifications when trap is sent to the destination. This option is valid only for SNMPv2.\n'\
                                        '    - Trap - Do not receive notifications when trap is sent to the destination.\n'
                                    templateVars["var_type"] = 'Trap Type'
                                    trap_type = variable_loop(**templateVars)
                                else:
                                    trap_type = 'Trap'

                                valid = False
                                while valid == False:
                                    destination_address = input(f'What is the SNMP Trap Destination Hostname/Address? ')
                                    if not destination_address == '':
                                        if re.search(r'^[0-9a-fA-F]+[:]+[0-9a-fA-F]$', destination_address) or \
                                            re.search(r'^(\d{1,3}\.){3}\d{1,3}$', destination_address):
                                            valid = validating_ucs.ip_address('SNMP Trap Destination', destination_address)
                                        else:
                                            valid = validating_ucs.dns_name('SNMP Trap Destination', destination_address)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please Re-enter the SNMP Trap Destination Hostname/Address.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                valid = False
                                while valid == False:
                                    port = input(f'Enter the Port to Assign to this Destination.  Valid Range is 1-65535.  [162]: ')
                                    if port == '':
                                        port = 162
                                    if re.search(r'[0-9]{1,4}', str(port)):
                                        valid = validating_ucs.snmp_port('SNMP Port', port, 1, 65535)
                                    else:
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Invalid Entry!  Please Enter a valid Port in the range of 1-65535.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')

                                if snmp_version == 'V3':
                                    snmp_destination = {
                                        'destination_address':destination_address,
                                        'enabled':True,
                                        'port':port,
                                        'trap_type':trap_type,
                                        'user':snmp_user,
                                        'version':snmp_version
                                    }
                                else:
                                    snmp_destination = {
                                        'community':community_string,
                                        'destination_address':destination_address,
                                        'enabled':True,
                                        'port':port,
                                        'trap_type':trap_type,
                                        'version':snmp_version
                                    }

                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                if snmp_version == 'V2':
                                    print(f'   community_string    = "Sensitive"')
                                print(f'   destination_address = "{destination_address}"')
                                print(f'   enable              = True')
                                print(f'   trap_type           = "{trap_type}"')
                                print(f'   snmp_version        = "{snmp_version}"')
                                if snmp_version == 'V3':
                                    print(f'   user                = "{snmp_user}"')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = False
                                while valid_confirm == False:
                                    confirm_v = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                                    if confirm_v == 'Y' or confirm_v == '':
                                        templateVars["trap_destinations"].append(snmp_destination)
                                        valid_exit = False
                                        while valid_exit == False:
                                            loop_exit = input(f'Would You like to Configure another SNMP Trap Destination?  Enter "Y" or "N" [N]: ')
                                            if loop_exit == 'Y':
                                                inner_loop_count += 1
                                                valid_confirm = True
                                                valid_exit = True
                                            elif loop_exit == 'N' or loop_exit == '':
                                                snmp_loop = True
                                                valid_confirm = True
                                                valid_exit = True
                                                valid_traps = True
                                            else:
                                                print(f'\n------------------------------------------------------\n')
                                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                                print(f'\n------------------------------------------------------\n')

                                    elif confirm_v == 'N':
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        print(f'  Starting Remote Host Configuration Over.')
                                        print(f'\n-------------------------------------------------------------------------------------------\n')
                                        valid_confirm = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                        elif question == 'N':
                            snmp_loop = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

                    templateVars["enabled"] = True
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    access_community_string = "Sensitive"')
                    print(f'    description             = {templateVars["descr"]}')
                    print(f'    enable_snmp             = {templateVars["enabled"]}')
                    print(f'    name                    = "{templateVars["name"]}"')
                    print(f'    snmp_community_access   = "{templateVars["community_access"]}"')
                    print(f'    snmp_engine_input_id    = "{templateVars["engine_input_id"]}"')
                    print(f'    snmp_port               = {templateVars["port"]}')
                    if len(templateVars["trap_destinations"]) > 0:
                        print(f'    snmp_trap_destinations = ''{')
                        for item in templateVars["trap_destinations"]:
                            for k, v in item.items():
                                if k == 'destination_address':
                                    print(f'      "{v}" = ''{')
                            for k, v in item.items():
                                if k == 'community':
                                    print(f'        community_string = "Sensitive"')
                                elif k == 'enabled':
                                    print(f'        enable           = {v}')
                                elif k == 'trap_type':
                                    print(f'        trap_type        = "{v}"')
                                elif k == 'port':
                                    print(f'        port             = {v}')
                                elif k == 'user':
                                    print(f'        user             = "{v}"')
                                elif k == 'version':
                                    print(f'        snmp_server      = "{v}"')
                            print(f'      ''}')
                        print(f'    ''}')
                    if len(templateVars["users"]) > 0:
                        print(f'    snmp_users = ''{')
                        for item in templateVars["users"]:
                            for k, v in item.items():
                                if k == 'name':
                                    print(f'      "{v}" = ''{')
                            for k, v in item.items():
                                if k == 'auth_password':
                                    print(f'        auth_password    = "Sensitive"')
                                elif k == 'auth_type':
                                    print(f'        auth_type        = "{v}"')
                                elif k == 'privacy_password':
                                    print(f'        privacy_password = "Sensitive"')
                                elif k == 'privacy_type':
                                    print(f'        privacy_type     = "{v}"')
                                elif k == 'security_level':
                                    print(f'        security_level   = "{v}"')
                            print(f'      ''}')
                        print(f'    ''}')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # SSH Policy Module
    #========================================
    def ssh_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'ssh'
        org = self.org
        policy_type = 'SSH Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ssh_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  An {policy_type} enables an SSH client to make a secure, encrypted connection. You can ')
            print(f'  create one or more SSH policies that contain a specific grouping of SSH properties for a ')
            print(f'  server or a set of servers.\n\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure an {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["enable_ssh"] = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Port used for secure shell access.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["ssh_port"] = input('What is the SSH Port?  [22]: ')
                        if templateVars["ssh_port"] == '':
                            templateVars["ssh_port"] = 22
                        if re.search(r'[\d]+', str(templateVars["ssh_port"])):
                            valid = validating_ucs.number_in_range('SSH Port', templateVars["ssh_port"], 1, 65535)
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  "{templateVars["ssh_port"]}" is not a valid port.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Number of seconds to wait before the system considers an SSH request to have timed out.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["ssh_timeout"] = input('What value do you want to set for the SSH Timeout?  [1800]: ')
                        if templateVars["ssh_timeout"] == '':
                            templateVars["ssh_timeout"] = 1800
                        if re.search(r'[\d]+', str(templateVars["ssh_timeout"])):
                            valid = validating_ucs.number_in_range('SSH Timeout', templateVars["ssh_timeout"], 60, 10800)
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  "{templateVars["ssh_timeout"]}" is not a valid value.  Must be between 60 and 10800')
                            print(f'\n-------------------------------------------------------------------------------------------\n')


                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'    description = "{templateVars["descr"]}"')
                    print(f'    enable_ssh  = {templateVars["enable_ssh"]}')
                    print(f'    name        = "{templateVars["name"]}"')
                    print(f'    ssh_port    = {templateVars["ssh_port"]}')
                    print(f'    ssh_timeout = "{templateVars["ssh_timeout"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Storage Policy Module
    #========================================
    def storage_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'storage'
        org = self.org
        policy_type = 'Storage Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'storage_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["priority"] = 'auto'
                    templateVars["receive"] = 'Disabled'
                    templateVars["send"] = 'Disabled'

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Switch Control Policy Module
    #========================================
    def switch_control_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'sw_ctrl'
        org = self.org
        policy_type = 'Switch Control Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'switch_control_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A Switch Control Policy will configure Unidirectional Link Detection Protocol and')
            print(f'  MAC Address Learning Settings for the UCS Domain Profile.')
            print(f'  We recommend the settings the wizard is setup to push.  So you will only be asked for')
            print(f'  the name and description for the Policy.  You only need one of these policies for')
            print(f'  Organization {org}.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                templateVars["mac_address_table_aging"] = 'Default'
                templateVars["mac_aging_time"] = 14500
                templateVars["udld_message_interval"] = 15
                templateVars["udld_recovery_action"] = "reset"
                templateVars["vlan_port_count_optimization"] = False

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description                  = "{templateVars["descr"]}"')
                print(f'    mac_address_table_aging      = "{templateVars["mac_address_table_aging"]}"')
                print(f'    mac_aging_time               = {templateVars["mac_aging_time"]}')
                print(f'    name                         = "{templateVars["name"]}"')
                print(f'    udld_message_interval        = {templateVars["udld_message_interval"]}')
                print(f'    udld_recovery_action         = "{templateVars["udld_recovery_action"]}"')
                print(f'    vlan_port_count_optimization = {templateVars["vlan_port_count_optimization"]}')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Syslog Policy Module
    #========================================
    def syslog_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'syslog'
        org = self.org
        policy_type = 'Syslog Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'syslog_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure domain and servers with remote syslog servers.')
            print(f'  You can configure up to two Remote Syslog Servers.')
            print(f'  This Policy is not required to standup a server but is a good practice for day 2 support.')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'syslog_severity.txt'
                    templateVars["var_description"] = '    Please Select the Local Minimum Severity.\n'\
                        '    - emergency\n'\
                        '    - alert\n'\
                        '    - critical (Intersight Critical)\n'\
                        '    - error (Intersight Major)\n'\
                        '    - warning (Defualt) - (Intersight Minor)\n'\
                        '    - notice (Intersight Warning)\n'\
                        '    - informational\n'\
                        '    - debug\n'
                    templateVars["var_type"] = 'Local Severity'
                    min_severity = variable_loop(**templateVars)

                    templateVars["local_logging"] = {'file':{'min_severity':min_severity}}

                    templateVars["remote_logging"] = {}
                    syslog_count = 1
                    syslog_loop = False
                    while syslog_loop == False:
                        valid = False
                        while valid == False:
                            hostname = input(f'Enter the Hostname/IP Address of the Remote Server: ')
                            if re.search(r'[a-zA-Z]+', hostname):
                                valid = validating_ucs.dns_name('Primary NTP Server', hostname)
                            else:
                                valid = validating_ucs.ip_address('Primary NTP Server', hostname)

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'syslog_severity.txt'
                        templateVars["var_description"] = '    Please Select the Minimum Severity to Report.\n'\
                            '    - emergency\n'\
                            '    - alert\n'\
                            '    - critical (Intersight Critical)\n'\
                            '    - error (Intersight Major)\n'\
                            '    - warning (Defualt) - (Intersight Minor)\n'\
                            '    - notice (Intersight Warning)\n'\
                            '    - informational\n'\
                            '    - debug\n'
                        templateVars["var_type"] = 'Remote Severity'
                        min_severity = variable_loop(**templateVars)

                        templateVars["multi_select"] = False
                        templateVars["policy_file"] = 'protocol.txt'
                        templateVars["var_description"] = '    Please Select the Protocol for the Remote Server.\n'
                        templateVars["var_type"] = 'Protocol'
                        protocol = variable_loop(**templateVars)

                        valid = False
                        while valid == False:
                            port = input(f'Enter the Port to Assign to this Policy.  Valid Range is 1-65535.  [514]: ')
                            if port == '':
                                port = 514
                            if re.search(r'[0-9]{1,4}', str(port)):
                                valid = validating_ucs.number_in_range('Port', port, 1, 65535)
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Invalid Entry!  Please Enter a valid Port in the range of 1-65535.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        remote_host = {
                            'enable':True,
                            'hostname':hostname,
                            'min_severity':min_severity,
                            'port':port,
                            'protocol':protocol
                        }
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Do you want to accept the following configuration?')
                        print(f'   hostname     = "{hostname}"')
                        print(f'   min_severity = "{min_severity}"')
                        print(f'   port         = {port}')
                        print(f'   protocol     = "{protocol}"')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        valid_confirm = False
                        while valid_confirm == False:
                            confirm_host = input('Enter "Y" or "N" [Y]: ')
                            if confirm_host == 'Y' or confirm_host == '':
                                if syslog_count == 1:
                                    templateVars['remote_logging'].update({'server1':remote_host})
                                if syslog_count == 2:
                                    templateVars['remote_logging'].update({'server2':remote_host})
                                if syslog_count == 1:
                                    valid_exit = False
                                    while valid_exit == False:
                                        remote_exit = input(f'Would You like to Configure another Remote Host?  Enter "Y" or "N" [Y]: ')
                                        if remote_exit == 'Y' or remote_exit == '':
                                            syslog_count += 1
                                            valid_confirm = True
                                            valid_exit = True
                                        elif remote_exit == 'N':
                                            syslog_loop = True
                                            valid_exit = True
                                        else:
                                            print(f'\n------------------------------------------------------\n')
                                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                            print(f'\n------------------------------------------------------\n')

                                else:
                                    syslog_loop = True
                                    valid_confirm = True

                            elif confirm_host == 'N':
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Starting Remote Host Configuration Over.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                syslog_loop = True
                                valid_confirm = True
                            else:
                                print(f'\n------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    description        = "{templateVars["descr"]}"')
                    print(f'    local_min_severity = "{min_severity}"')
                    print(f'    name               = "{templateVars["name"]}"')
                    print(f'    remote_clients = [')
                    item_count = 1
                    print(templateVars["remote_logging"])
                    for key, value in templateVars["remote_logging"].items():
                        print(f'      ''{')
                        for k, v in value.items():
                            if k == 'enable':
                                print(f'        enabled      = {"%s".lower() % (v)}')
                            elif k == 'hostname':
                                print(f'        hostname     = "{v}"')
                            elif k == 'min_severity':
                                print(f'        min_severity = "{v}"')
                            elif k == 'port':
                                print(f'        port         = {v}')
                            elif k == 'protocol':
                                print(f'        protocol     = "{v}"')
                        print(f'      ''}')
                        item_count += 1
                    print(f'    ]')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # System QoS Policy Module
    #========================================
    def system_qos_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'qos'
        org = self.org
        policy_type = 'System QoS Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'system_qos_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A System QoS Policy will configure the QoS Policies for the UCS Domain Profile')
            print(f'  These Queues are represented by the following Priorities:')
            print(f'    - Platinum')
            print(f'    - Gold')
            print(f'    - FC')
            print(f'    - Silver')
            print(f'    - Bronze')
            print(f'    - Best Effort')
            print(f'  For the System MTU we recommend to set the MTU to Jumbo frames unless you are unable.')
            print(f'  to configure jumbo frames in your network.  Any traffic that is moving large')
            print(f'  amounts of packets through the network will be improved with Jumbo MTU support.')
            print(f'  Beyond the System MTU, we recommend you utilize the default parameters of this wizard.')
            print(f'  You only need one of these policies for Organization {org}.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                valid = False
                while valid == False:
                    mtu = input('Do you want to enable Jumbo MTU?  Enter "Y" or "N" [Y]: ')
                    if mtu == '' or mtu == 'Y':
                        templateVars["mtu"] = 9216
                        valid = True
                    elif mtu == 'N':
                        templateVars["mtu"] = 1500
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Option.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                domain_mtu = templateVars["mtu"]

                templateVars["Platinum"] = {
                    'bandwidth_percent':20,
                    'cos':5,
                    'mtu':templateVars["mtu"],
                    'multicast_optimize':False,
                    'packet_drop':False,
                    'priority':'Platinum',
                    'state':'Enabled',
                    'weight':10,
                }
                templateVars["Gold"] = {
                    'bandwidth_percent':19,
                    'cos':4,
                    'mtu':templateVars["mtu"],
                    'multicast_optimize':False,
                    'packet_drop':True,
                    'priority':'Gold',
                    'state':'Enabled',
                    'weight':9,
                }
                templateVars["FC"] = {
                    'bandwidth_percent':21,
                    'cos':3,
                    'mtu':2240,
                    'multicast_optimize':False,
                    'packet_drop':False,
                    'priority':'FC',
                    'state':'Enabled',
                    'weight':10,
                }
                templateVars["Silver"] = {
                    'bandwidth_percent':16,
                    'cos':2,
                    'mtu':templateVars["mtu"],
                    'multicast_optimize':False,
                    'packet_drop':True,
                    'priority':'Silver',
                    'state':'Enabled',
                    'weight':8,
                }
                templateVars["Bronze"] = {
                    'bandwidth_percent':14,
                    'cos':1,
                    'mtu':templateVars["mtu"],
                    'multicast_optimize':False,
                    'packet_drop':True,
                    'priority':'Bronze',
                    'state':'Enabled',
                    'weight':7,
                }
                templateVars["Best Effort"] = {
                    'bandwidth_percent':10,
                    'cos':255,
                    'mtu':templateVars["mtu"],
                    'multicast_optimize':False,
                    'packet_drop':True,
                    'priority':'Best Effort',
                    'state':'Enabled',
                    'weight':5,
                }

                templateVars["classes"] = []
                priorities = ['Platinum', 'Gold', 'FC', 'Silver', 'Bronze', 'Best Effort']

                for priority in priorities:
                    templateVars["classes"].append(templateVars[priority])
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    description = "{templateVars["descr"]}"')
                print(f'    name        = "{templateVars["name"]}"')
                print('    classes = {')
                for item in templateVars["classes"]:
                    for k, v in item.items():
                        if k == 'priority':
                            print(f'      "{v}" = ''{')
                    for k, v in item.items():
                        if k == 'bandwidth_percent':
                            print(f'        bandwidth_percent  = {v}')
                        elif k == 'cos':
                            print(f'        cos                = {v}')
                        elif k == 'mtu':
                            print(f'        mtu                = {v}')
                        elif k == 'multicast_optimize':
                            print(f'        multicast_optimize = {v}')
                        elif k == 'packet_drop':
                            print(f'        packet_drop        = {v}')
                        elif k == 'state':
                            print(f'        state              = "{v}"')
                        elif k == 'weight':
                            print(f'        weight             = {v}')
                    print('      }')
                print('    }')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Thermal Policy Module
    #========================================
    def thermal_policies(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'Thermal Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'thermal_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure the Cooling/FAN Policy for Chassis.  We recommend ')
            print(f'  Balanced for a 5108 and Acoustic for a 9508 Chassis, as of this writing.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'chassis_type.txt'
                templateVars["var_description"] = '   Please Select the Type of Chassis this Thermal Policy is for.'
                templateVars["var_type"] = 'Chassis Type'
                chassis_type = variable_loop(**templateVars)

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, chassis_type)
                else:
                    name = '%s_%s' % (org, chassis_type)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                if chassis_type == '5108':
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'thermal_5108.txt'
                    templateVars["var_description"] = '    Please Select the Thermal Policy to apply to the system\n'\
                        '      - Balanced - The fans run faster when needed based on the heat generated by the chassis. When possible, the fans returns to the minimum required speed.\n'\
                        '      - LowPower - The Fans run at the minimum speed required to keep the chassis cool.\n'
                else:
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'thermal_9508.txt'
                    templateVars["var_description"] = '   Please Select the Thermal Policy to apply to the system\n'\
                        '      - Acoustic - The fan speed is reduced to reduce noise levels in acoustic-sensitive environments.\n'\
                        '      - Balanced - The fans run faster when needed based on the heat generated by the chassis. When possible, the fans returns to the minimum required speed.\n'\
                        '      - LowPower - The Fans run at the minimum speed required to keep the chassis cool.\n'\
                        '      - HighPower - The fans are kept at higher speed to emphasizes performance over power consumption.\n'\
                        '      - MaximumPower - The fans are always kept at maximum speed. This option provides the most cooling and consumes the most power.\n'
                templateVars["var_type"] = 'Chassis Type'
                templateVars["fan_control_mode"] = variable_loop(**templateVars)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'   description      = "{templateVars["descr"]}"')
                print(f'   name             = "{templateVars["name"]}"')
                print(f'   fan_control_mode = "{templateVars["fan_control_mode"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # UCS Chassis Profile Module
    #========================================
    def ucs_chassis_profiles(self):
        name_prefix = self.name_prefix
        name_suffix = 'chassis'
        org = self.org
        policy_type = 'UCS Chassis Profile'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ucs_chassis_profiles'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s' % (name_prefix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'action.txt'
                    templateVars["var_description"] = '    Please Choose the Action to Perform on the Chassis with this Profile:\n'\
                        '    - Deploy - will deploy the profile.\n'\
                        '    - No-op - will not deploy the profile.\n'\
                        '    - Unassign - will detach the profile from the hardware.\n\n'
                    templateVars["var_type"] = 'Action'
                    templateVars["action"] = variable_loop(**templateVars)

                    valid = False
                    while valid == False:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Note: If you do not have the Serial Number at this time you can manually add it to the:')
                        print(f'        - ucs_chassis_profiles/ucs_chassis_profiles.auto.tfvars file later.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        templateVars["serial_number"] = input('What is the Serial Number of the Chassis? [press enter to skip]: ')
                        if templateVars["serial_number"] == '':
                            valid = True
                        elif re.fullmatch(r'^[A-Z]{3}[2-3][\d]([0][1-9]|[1-4][0-9]|[5][1-3])[\dA-Z]{4}$', templateVars["serial_number"]):
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Serial Number.  "{templateVars["serial_number"]}" is not a valid serial.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    policy_list = [
                        'policies.imc_access_policies.imc_access_policy',
                        'policies.power_policies.power_policy',
                        'policies.snmp_policies.snmp_policy',
                        'policies.thermal_policies.thermal_policy'
                    ]
                    templateVars["allow_opt_out"] = True
                    for policy in policy_list:
                        policy_short = policy.split('.')[2]
                        templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        templateVars.update(policyData)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    action            = "No-op"')
                    if not templateVars["serial_number"] == '':
                        print(f'    assign_chassis    = True')
                    else:
                        print(f'    assign_chassis    = False')
                    print(f'    name              = "{templateVars["name"]}"')
                    print(f'    imc_access_policy = "{templateVars["imc_access_policy"]}"')
                    print(f'    power_policy      = "{templateVars["power_policy"]}"')
                    print(f'    serial_number     = "{templateVars["serial_number"]}"')
                    print(f'    snmp_policy       = "{templateVars["snmp_policy"]}"')
                    print(f'    thermal_policy    = "{templateVars["thermal_policy"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # UCS Domain Profile Module
    #========================================
    def ucs_domain_profiles(self):
        name_prefix = self.name_prefix
        name_suffix = 'ucs'
        org = self.org
        policy_type = 'UCS Domain Profile'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ucs_domain_profiles'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s' % (name_prefix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'action.txt'
                    templateVars["var_description"] = '    Please Choose the Action to Perform on the Domain with this Profile:\n'\
                        '    - Deploy - will deploy the profile.\n'\
                        '    - No-op - will not deploy the profile.\n'\
                        '    - Unassign - will detach the profile from the hardware.\n\n'
                    templateVars["var_type"] = 'Action'
                    templateVars["action"] = variable_loop(**templateVars)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Note: If you do not have the Serial Number at this time you can manually add it to the:')
                    print(f'        - ucs_domain_profiles/ucs_domain_profiles.auto.tfvars file later.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["serial_number_fabric_a"] = input('What is the Serial Number of Fabric A? [press enter to skip]: ')
                        if templateVars["serial_number_fabric_a"] == '':
                            valid = True
                        elif re.fullmatch(r'^[A-Z]{3}[2-3][\d]([0][1-9]|[1-4][0-9]|[5][1-3])[\dA-Z]{4}$', templateVars["serial_number_fabric_a"]):
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Serial Number.  "{templateVars["serial_number_fabric_a"]}" is not a valid serial.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["serial_number_fabric_b"] = input('What is the Serial Number of Fabric B? [press enter to skip]: ')
                        if templateVars["serial_number_fabric_b"] == '':
                            valid = True
                        elif re.fullmatch(r'^[A-Z]{3}[2-3][\d]([0][1-9]|[1-4][0-9]|[5][1-3])[\dA-Z]{4}$', templateVars["serial_number_fabric_b"]):
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Serial Number.  "{templateVars["serial_number_fabric_b"]}" is not a valid serial.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    policy_list = [
                        'policies.network_connectivity_policies.network_connectivity_policy',
                        'policies.ntp_policies.ntp_policy',
                        'policies.snmp_policies.snmp_policy',
                        'policies.switch_control_policies.switch_control_policy',
                        'policies.syslog_policies.syslog_policy',
                        'policies.system_qos_policies.system_qos_policy'
                    ]
                    templateVars["allow_opt_out"] = True
                    for policy in policy_list:
                        policy_short = policy.split('.')[2]
                        templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        templateVars.update(policyData)

                    policy_list = [
                        'policies.port_policies.port_policy',
                        'policies_vlans.vlan_policies.vlan_policy',
                        'policies.vsan_policies.vsan_policy'
                    ]
                    templateVars["allow_opt_out"] = False
                    for policy in policy_list:
                        policy_long = policy.split('.')[1]
                        policy_short = policy.split('.')[2]
                        x = policy_short.split('_')
                        policy_description = []
                        for y in x:
                            y = y.capitalize()
                            policy_description.append(y)
                        policy_description = " ".join(policy_description)

                        templateVars[policy_long] = {}
                        # templateVars["policy"] = '%s Fabric A' % (policy_description)
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  !!! Select the {policy_description} for Fabric A !!!')
                        fabric_a,policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        # templateVars["policy"] = '%s Fabric B' % (policy_description)
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  !!! Select the {policy_description} for Fabric B !!!')
                        fabric_b,policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        templateVars[policy_long].update({'fabric_a':fabric_a})
                        templateVars[policy_long].update({'fabric_b':fabric_b})
                        if policy_long == 'port_policies':
                            device_model_a = policyData['port_policies'][0][fabric_a][0]['device_model']
                            device_model_b = policyData['port_policies'][0][fabric_b][0]['device_model']
                            if not device_model_a == device_model_b:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  !!! Error.  Device Model for the port Policies does not match !!!')
                                print(f'  Fabric A Port Policy device_model is {device_model_a}.')
                                print(f'  Fabric B Port Policy device_model is {device_model_b}.')
                                print(f'  The script is going to set the device_model to match Fabric A for now but you should.')
                                print(f'  either reject this configuration assuming you mistakenly chose non-matching port policies.')
                                print(f'  or re-run the port-policy wizard again to correct the configuration.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                templateVars["device_model"] = device_model_a
                            else:
                                templateVars["device_model"] = device_model_a


                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    action                      = "No-op"')
                    if not (templateVars["serial_number_fabric_a"] == '' and templateVars["serial_number_fabric_a"] == ''):
                        print(f'    assign_switches             = True')
                    else:
                        print(f'    assign_switches             = False')
                    print(f'    device_model                = {templateVars["device_model"]}')
                    print(f'    name                        = "{templateVars["name"]}"')
                    print(f'    network_connectivity_policy = "{templateVars["network_connectivity_policy"]}"')
                    print(f'    ntp_policy                  = "{templateVars["ntp_policy"]}"')
                    print(f'    port_policy_fabric_a        = "{templateVars["port_policies"]["fabric_a"]}"')
                    print(f'    port_policy_fabric_b        = "{templateVars["port_policies"]["fabric_b"]}"')
                    print(f'    serial_number_fabric_a      = "{templateVars["serial_number_fabric_a"]}"')
                    print(f'    serial_number_fabric_b      = "{templateVars["serial_number_fabric_b"]}"')
                    print(f'    snmp_policy                 = "{templateVars["snmp_policy"]}"')
                    print(f'    switch_control_policy       = "{templateVars["switch_control_policy"]}"')
                    print(f'    syslog_policy               = "{templateVars["syslog_policy"]}"')
                    print(f'    system_qos_policy           = "{templateVars["system_qos_policy"]}"')
                    print(f'    vlan_policy_fabric_a        = "{templateVars["vlan_policies"]["fabric_a"]}"')
                    print(f'    vlan_policy_fabric_b        = "{templateVars["vlan_policies"]["fabric_b"]}"')
                    print(f'    vsan_policy_fabric_a        = "{templateVars["vsan_policies"]["fabric_a"]}"')
                    print(f'    vsan_policy_fabric_b        = "{templateVars["vsan_policies"]["fabric_b"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # UCS Server Profile Module
    #========================================
    def ucs_server_profiles(self):
        name_prefix = self.name_prefix
        name_suffix = 'server'
        org = self.org
        policy_type = 'UCS Server Profile'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ucs_server_profiles'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s' % (name_prefix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                templateVars["multi_select"] = False
                templateVars["policy_file"] = 'action.txt'
                templateVars["var_description"] = '    Please Choose the Action to Perform on the Server with this Profile:\n'\
                    '    - Deploy - will deploy the profile.\n'\
                    '    - No-op - will not deploy the profile.\n'\
                    '    - Unassign - will detach the profile from the hardware.\n\n'
                templateVars["var_type"] = 'Action'
                templateVars["action"] = variable_loop(**templateVars)

                valid = False
                while valid == False:
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Note: If you do not have the Serial Number at this time you can manually add it to the:')
                    print(f'        - ucs_server_profiles/ucs_server_profiles.auto.tfvars file later.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    templateVars["serial_number"] = input('What is the Serial Number of the Server? [press enter to skip]: ')
                    if templateVars["serial_number"] == '':
                        valid = True
                    elif re.fullmatch(r'^[A-Z]{3}[2-3][\d]([0][1-9]|[1-4][0-9]|[5][1-3])[\dA-Z]{4}$', templateVars["serial_number"]):
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Serial Number.  "{templateVars["serial_number"]}" is not a valid serial.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    server_template = input('Do you want to Associate to a UCS Server Profile Template?  Enter "Y" or "N" [Y]: ')
                    if server_template == '' or server_template == 'Y':
                        policy_list = [
                            'ucs_server_profiles.ucs_server_profile_templates.ucs_server_profile_template'
                        ]
                        templateVars["allow_opt_out"] = False
                        for policy in policy_list:
                            policy_short = policy.split('.')[2]
                            templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                            templateVars.update(policyData)
                            server_template = True
                            valid = True
                    elif server_template == 'N':
                        server_template = False
                        valid = True
                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

                if server_template == False:
                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'target_platform.txt'
                    templateVars["var_description"] = '    The platform for which the server profile is applicable. It can either be:\n'
                    templateVars["var_type"] = 'Target Platform'
                    target_platform = variable_loop(**templateVars)
                    templateVars["target_platform"] = target_platform

                    if templateVars["target_platform"] == 'FIAttached':
                        policy_list = [
                            #___________________________
                            #
                            # Compute Configuration
                            #___________________________
                            'policies.bios_policies.bios_policy',
                            'policies.boot_order_policies.boot_order_policy',
                            'policies.power_policies.certificate_management_policy',
                            'policies.virtual_media_policies.certificate_management_policy'
                            #___________________________
                            #
                            # Management Configuration
                            #___________________________
                            'policies.certificate_management_policies.certificate_management_policy',
                            'policies.imc_access_policies.certificate_management_policy',
                            'policies.ipmi_over_lan_policies.certificate_management_policy',
                            'policies.local_user_policies.certificate_management_policy',
                            'policies.serial_over_lan_policies.certificate_management_policy',
                            'policies.snmp_policies.certificate_management_policy',
                            'policies.syslog_policies.certificate_management_policy',
                            'policies.virtual_kvm_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Storage Configuration
                            #___________________________
                            'policies.sd_card_policies.certificate_management_policy',
                            'policies.storage_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Network Configuration
                            #___________________________
                            'policies.lan_connectivity_policies.certificate_management_policy',
                            'policies.san_connectivity_policies.certificate_management_policy',
                        ]
                    elif templateVars["target_platform"] == 'Standalone':
                        policy_list = [
                            #___________________________
                            #
                            # Compute Configuration
                            #___________________________
                            'policies.bios_policies.bios_policy',
                            'policies.boot_order_policies.boot_order_policy',
                            'policies.persistent_memory_policies.certificate_management_policy',
                            'policies.virtual_media_policies.certificate_management_policy'
                            #___________________________
                            #
                            # Management Configuration
                            #___________________________
                            'policies.device_connector_policies.certificate_management_policy',
                            'policies.ipmi_over_lan_policies.certificate_management_policy',
                            'policies.ldap_policies_policies.certificate_management_policy',
                            'policies.local_user_policies.certificate_management_policy',
                            'policies.network_connectivity_policies.certificate_management_policy',
                            'policies.ntp_policies.certificate_management_policy',
                            'policies.serial_over_lan_policies.certificate_management_policy',
                            'policies.smtp_policies.certificate_management_policy',
                            'policies.snmp_policies.certificate_management_policy',
                            'policies.ssh_policies.certificate_management_policy',
                            'policies.syslog_policies.certificate_management_policy',
                            'policies.virtual_kvm_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Storage Configuration
                            #___________________________
                            'policies.sd_card_policies.certificate_management_policy',
                            'policies.storage_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Network Configuration
                            #___________________________
                            'policies.adapter_configuration_policies.adapter_configuration_policy',
                            'policies.lan_connectivity_policies.certificate_management_policy',
                            'policies.san_connectivity_policies.certificate_management_policy',
                        ]
                    templateVars["allow_opt_out"] = True
                    for policy in policy_list:
                        policy_short = policy.split('.')[2]
                        templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        templateVars.update(policyData)

                if templateVars["serial_number"] == '':
                    templateVars["assign_server"] = False
                else:
                    templateVars["assign_server"] = True
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'    action          = "{templateVars["action"]}"')
                print(f'    assign_server   = {templateVars["assign_server"]}')
                print(f'    description     = "{templateVars["descr"]}"')
                print(f'    name            = "{templateVars["name"]}"')
                print(f'    serial_number   = "{templateVars["serial_number"]}"')
                if server_template == False:
                    print(f'    target_platform = "{templateVars["target_platform"]}"')
                if server_template == True:
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Server Template')
                    print(f'    #___________________________"')
                    print(f'    ucs_server_profile_template = "{templateVars["ucs_server_profile_template"]}"')
                if server_template == False:
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Compute Configuration')
                    print(f'    #___________________________"')
                    print(f'    bios_policy                = "{templateVars["bios_policy"]}"')
                    print(f'    boot_order_policy          = "{templateVars["boot_order_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    persistent_memory_policies = "{templateVars["persistent_memory_policies"]}"')
                    if target_platform == 'FIAttached':
                        print(f'    power_policy               = "{templateVars["power_policy"]}"')
                    print(f'    virtual_media_policy       = "{templateVars["virtual_media_policy"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Management Configuration')
                    print(f'    #___________________________"')
                    if target_platform == 'FIAttached':
                        print(f'    certificate_management_policy = "{templateVars["pcertificate_management_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    device_connector_policies     = "{templateVars["device_connector_policies"]}"')
                    if target_platform == 'FIAttached':
                        print(f'    imc_access_policy             = "{templateVars["imc_access_policy"]}"')
                    print(f'    ipmi_over_lan_policy          = "{templateVars["ipmi_over_lan_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    ldap_policies                 = "{templateVars["ldap_policies"]}"')
                    print(f'    local_user_policy             = "{templateVars["local_user_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    network_connectivity_policy   = "{templateVars["network_connectivity_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    ntp_policy                    = "{templateVars["ntp_policy"]}"')
                    print(f'    serial_over_lan_policy        = "{templateVars["serial_over_lan_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    smtp_policy                   = "{templateVars["smtp_policy"]}"')
                    print(f'    snmp_policy                   = "{templateVars["snmp_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    ssh_policy                    = "{templateVars["ssh_policy"]}"')
                    print(f'    syslog_policy                 = "{templateVars["syslog_policy"]}"')
                    print(f'    virtual_kvm_policy            = "{templateVars["virtual_kvm_policy"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Storage Configuration')
                    print(f'    #___________________________"')
                    print(f'    sd_card_policy = "{templateVars["sd_card_policy"]}"')
                    print(f'    storage_policy = "{templateVars["storage_policy"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Network Configuration')
                    print(f'    #___________________________"')
                    if target_platform == 'Standalone':
                        print(f'    adapter_configuration_policy = "{templateVars["adapter_configuration_policy"]}"')
                    print(f'    lan_connectivity_policy      = "{templateVars["lan_connectivity_policy"]}"')
                    print(f'    san_connectivity_policy      = "{templateVars["san_connectivity_policy"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # UCS Server Profile Template Module
    #========================================
    def ucs_server_profile_templates(self):
        name_prefix = self.name_prefix
        name_suffix = 'template'
        org = self.org
        policy_type = 'UCS Server Profile Template'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'ucs_server_profile_templates'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["multi_select"] = False
                    templateVars["policy_file"] = 'target_platform.txt'
                    templateVars["var_description"] = '    The platform for which the server profile is applicable. It can either be:\n'
                    templateVars["var_type"] = 'Target Platform'
                    target_platform = variable_loop(**templateVars)
                    templateVars["target_platform"] = target_platform

                    if templateVars["target_platform"] == 'FIAttached':
                        policy_list = [
                            #___________________________
                            #
                            # Compute Configuration
                            #___________________________
                            'policies.bios_policies.bios_policy',
                            'policies.boot_order_policies.boot_order_policy',
                            'policies.power_policies.certificate_management_policy',
                            'policies.virtual_media_policies.certificate_management_policy'
                            #___________________________
                            #
                            # Management Configuration
                            #___________________________
                            'policies.certificate_management_policies.certificate_management_policy',
                            'policies.imc_access_policies.certificate_management_policy',
                            'policies.ipmi_over_lan_policies.certificate_management_policy',
                            'policies.local_user_policies.certificate_management_policy',
                            'policies.serial_over_lan_policies.certificate_management_policy',
                            'policies.snmp_policies.certificate_management_policy',
                            'policies.syslog_policies.certificate_management_policy',
                            'policies.virtual_kvm_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Storage Configuration
                            #___________________________
                            'policies.sd_card_policies.certificate_management_policy',
                            'policies.storage_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Network Configuration
                            #___________________________
                            'policies.lan_connectivity_policies.certificate_management_policy',
                            'policies.san_connectivity_policies.certificate_management_policy',
                        ]
                    elif templateVars["target_platform"] == 'Standalone':
                        policy_list = [
                            #___________________________
                            #
                            # Compute Configuration
                            #___________________________
                            'policies.bios_policies.bios_policy',
                            'policies.boot_order_policies.boot_order_policy',
                            'policies.persistent_memory_policies.certificate_management_policy',
                            'policies.virtual_media_policies.certificate_management_policy'
                            #___________________________
                            #
                            # Management Configuration
                            #___________________________
                            'policies.device_connector_policies.certificate_management_policy',
                            'policies.ipmi_over_lan_policies.certificate_management_policy',
                            'policies.ldap_policies_policies.certificate_management_policy',
                            'policies.local_user_policies.certificate_management_policy',
                            'policies.network_connectivity_policies.certificate_management_policy',
                            'policies.ntp_policies.certificate_management_policy',
                            'policies.serial_over_lan_policies.certificate_management_policy',
                            'policies.smtp_policies.certificate_management_policy',
                            'policies.snmp_policies.certificate_management_policy',
                            'policies.ssh_policies.certificate_management_policy',
                            'policies.syslog_policies.certificate_management_policy',
                            'policies.virtual_kvm_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Storage Configuration
                            #___________________________
                            'policies.sd_card_policies.certificate_management_policy',
                            'policies.storage_policies.certificate_management_policy',
                            #___________________________
                            #
                            # Network Configuration
                            #___________________________
                            'policies.adapter_configuration_policies.adapter_configuration_policy',
                            'policies.lan_connectivity_policies.certificate_management_policy',
                            'policies.san_connectivity_policies.certificate_management_policy',
                        ]
                    templateVars["allow_opt_out"] = True
                    for policy in policy_list:
                        policy_short = policy.split('.')[2]
                        templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                        templateVars.update(policyData)

                    print(templateVars)
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    description     = "{templateVars["descr"]}"')
                    print(f'    name            = "{templateVars["name"]}"')
                    print(f'    target_platform = "{templateVars["target_platform"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Compute Configuration')
                    print(f'    #___________________________"')
                    print(f'    bios_policy                = "{templateVars["bios_policy"]}"')
                    print(f'    boot_order_policy          = "{templateVars["boot_order_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    persistent_memory_policies = "{templateVars["persistent_memory_policies"]}"')
                    if target_platform == 'FIAttached':
                        print(f'    power_policy               = "{templateVars["power_policy"]}"')
                    print(f'    virtual_media_policy       = "{templateVars["virtual_media_policy"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Management Configuration')
                    print(f'    #___________________________"')
                    if target_platform == 'FIAttached':
                        print(f'    certificate_management_policy = "{templateVars["pcertificate_management_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    device_connector_policies     = "{templateVars["device_connector_policies"]}"')
                    if target_platform == 'FIAttached':
                        print(f'    imc_access_policy             = "{templateVars["imc_access_policy"]}"')
                    print(f'    ipmi_over_lan_policy          = "{templateVars["ipmi_over_lan_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    ldap_policies                 = "{templateVars["ldap_policies"]}"')
                    print(f'    local_user_policy             = "{templateVars["local_user_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    network_connectivity_policy   = "{templateVars["network_connectivity_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    ntp_policy                    = "{templateVars["ntp_policy"]}"')
                    print(f'    serial_over_lan_policy        = "{templateVars["serial_over_lan_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    smtp_policy                   = "{templateVars["smtp_policy"]}"')
                    print(f'    snmp_policy                   = "{templateVars["snmp_policy"]}"')
                    if target_platform == 'Standalone':
                        print(f'    ssh_policy                    = "{templateVars["ssh_policy"]}"')
                    print(f'    syslog_policy                 = "{templateVars["syslog_policy"]}"')
                    print(f'    virtual_kvm_policy            = "{templateVars["virtual_kvm_policy"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Storage Configuration')
                    print(f'    #___________________________"')
                    print(f'    sd_card_policy = "{templateVars["sd_card_policy"]}"')
                    print(f'    storage_policy = "{templateVars["storage_policy"]}"')
                    print(f'    #___________________________"')
                    print(f'    #')
                    print(f'    # Network Configuration')
                    print(f'    #___________________________"')
                    if target_platform == 'Standalone':
                        print(f'    adapter_configuration_policy = "{templateVars["adapter_configuration_policy"]}"')
                    print(f'    lan_connectivity_policy      = "{templateVars["lan_connectivity_policy"]}"')
                    print(f'    san_connectivity_policy      = "{templateVars["san_connectivity_policy"]}"')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # UUID Pools Module
    #========================================
    def uuid_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'uuid_pool'
        org = self.org
        policy_type = 'UUID Pool'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'uuid_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  The Universally Unique Identifier (UUID) are written in 5 groups of hexadecimal digits')
            print(f'  separated by hyphens.  The length of each group is: 8-4-4-4-12. UUIDs are fixed length.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}.  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the Index for the value to select [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        templateVars['prefix'] = input(f'\nWhat is the UUID Prefix you would like to assign to the Pool?  [000025B5-0000-0000]: ')
                        if templateVars['prefix'] == '':
                            templateVars['prefix'] = '000025B5-0000-0000'
                        valid = validating_ucs.uuid_suffix('UUID Pool From', templateVars['prefix'])

                    valid = False
                    while valid == False:
                        pool_from = input(f'\nWhat is the first Suffix in the Block?  [0000-000000000000]: ')
                        if pool_from == '':
                            pool_from = '0000-000000000000'
                        valid = validating_ucs.uuid_suffix('UUID Pool From', pool_from)

                    valid = False
                    while valid == False:
                        pool_size = input(f'\nWhat is the size of the Block?  [512]: ')
                        if pool_size == '':
                            pool_size = '512'
                        valid_size = validating_ucs.number_in_range('UUID Pool Size', pool_size, 1, 1000)

                    templateVars["uuid_blocks"] = [
                        {
                            'from':pool_from,
                            'size':pool_size
                        }
                    ]
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'    assignment_order = "{templateVars["assignment_order"]}"')
                    print(f'    description      = "{templateVars["descr"]}"')
                    print(f'    name             = "{templateVars["name"]}"')
                    print(f'    prefix           = "{templateVars["prefix"]}"')
                    print(f'    uuid_blocks = [')
                    for i in templateVars["iqn_blocks"]:
                        print(f'      ''{')
                        for k, v in i.items():
                            if k == 'from':
                                print(f'        from   = {v}')
                            elif k == 'size':
                                print(f'        size   = {v}')
                        print(f'      ''}')
                    print(f'    ]')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Do you want to accept the above configuration?  Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Virtual KVM Policy Module
    #========================================
    def virtual_kvm_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vkvm'
        org = self.org
        policy_type = 'Virtual KVM Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'virtual_kvm_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  A {policy_type} will configure the Server for KVM access.  Settings include:')
            print(f'   - Local Server Video - If enabled, displays KVM on any monitor attached to the server.')
            print(f'   - Video Encryption - encrypts all video information sent through KVM.')
            print(f'   - Remote Port - The port used for KVM communication. Range is 1 to 65535.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:

                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["enable_virtual_kvm"] = True
                templateVars["maximum_sessions"] = 4

                valid = False
                while valid == False:
                    local_video = input('Do you want to Display KVM on Monitors attached to the Server?  Enter "Y" or "N" [Y]: ')
                    if local_video == '' or local_video == 'Y':
                        templateVars["enable_local_server_video"] = True
                        valid = True
                    elif local_video == 'N':
                        templateVars["enable_local_server_video"] = False
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    video_encrypt = input('Do you want to Enable video Encryption?  Enter "Y" or "N" [Y]: ')
                    if video_encrypt == '' or video_encrypt == 'Y':
                        templateVars["enable_video_encryption"] = True
                        valid = True
                    elif video_encrypt == 'N':
                        templateVars["enable_video_encryption"] = False
                        valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                valid = False
                while valid == False:
                    templateVars["remote_port"] = input('What is the Port you would like to Assign for Remote Access?\n'
                        'This should be a value between 1024-65535. [2068]: ')
                    if templateVars["remote_port"] == '':
                        templateVars["remote_port"] = 2068
                    valid = validating_ucs.number_in_range('Remote Port', templateVars["remote_port"], 1, 65535)

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'   description               = "{templateVars["descr"]}"')
                print(f'   enable_local_server_video = {templateVars["enable_local_server_video"]}')
                print(f'   enable_video_encryption   = {templateVars["enable_video_encryption"]}')
                print(f'   enable_virtual_kvm        = {templateVars["enable_virtual_kvm"]}')
                print(f'   maximum_sessions          = {templateVars["maximum_sessions"]}')
                print(f'   name                      = "{templateVars["name"]}"')
                print(f'   remote_port               = "{templateVars["remote_port"]}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # Virtual Media Policy Module
    #========================================
    def virtual_media_policies(self):
        name_prefix = self.name_prefix
        name_suffix = 'vmedia'
        org = self.org
        policy_type = 'Virtual Media Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'virtual_media_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    templateVars["priority"] = 'auto'
                    templateVars["receive"] = 'Disabled'
                    templateVars["send"] = 'Disabled'

                    # Write Policies to Template File
                    templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                    write_to_template(self, **templateVars)

                    exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
                    if exit_answer == 'N' or exit_answer == '':
                        policy_loop = True
                        configure_loop = True
            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # VLAN Policy Module
    #========================================
    def vlan_policies(self):
        vlan_policies_vlans = []
        name_prefix = self.name_prefix
        name_suffix = 'vlans'
        org = self.org
        policy_type = 'VLAN Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'vlan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

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
            print(f'                  as Disjoint Layer 2 is not yet supported.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            policy_loop = False
            while policy_loop == False:
                if not name_prefix == '':
                    name = '%s_%s' % (name_prefix, name_suffix)
                else:
                    name = '%s_%s' % (org, name_suffix)

                templateVars["name"] = policy_name(name, policy_type)
                templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                templateVars["auto_allow_on_uplinks"] = True

                valid = False
                while valid == False:
                    vlan_list = '%s' % (input(f'Enter the VLAN or List of VLANs to add to {templateVars["name"]}: '))
                    if not vlan_list == '':
                        vlan_list_expanded = vlan_list_full(vlan_list)
                        valid_vlan = True
                        for vlan in vlan_list_expanded:
                            valid_vlan = validating_ucs.number_in_range('VLAN ID', vlan, 1, 4094)
                            if valid_vlan == False:
                                break
                        native_count = 0
                        native_vlan = ''
                        native_name = ''
                        if valid_vlan == True:
                            valid_name = False
                            while valid_name == False:
                                if len(vlan_list_expanded) == 1:
                                    vlan_name = '%s' % (input(f'Enter the Name you want to assign to "{vlan_list}": '))
                                    valid_name = validating_ucs.name_rule('VLAN Name', vlan_name, 1, 62)
                                else:
                                    vlan_name = '%s' % (input(f'Enter the Prefix Name you want to assign to "{vlan_list}": '))
                                    valid_name = validating_ucs.name_rule('VLAN Name', vlan_name, 1, 55)
                            native_vlan = input('Do you want to configure one of the VLANs as a Native VLAN? [press enter to skip]:')
                        if not native_vlan == '' and valid_vlan == True:
                            for vlan in vlan_list_expanded:
                                if int(native_vlan) == int(vlan):
                                    native_count = 1
                            if native_count == 1:
                                valid_name = False
                                while valid_name == False:
                                    native_name = '%s' % (input(f'Enter the Name to assign to the Native VLAN {native_vlan}.  [default]: '))
                                    if native_name == '':
                                        native_name = 'default'
                                    valid_name = validating_ucs.name_rule('VLAN Name', vlan_name, 1, 62)
                                valid = True
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Error!! The Native VLAN was not in the Allowed List.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        elif valid_vlan == True:
                            valid = True
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  The allowed vlan list can be in the format of:')
                        print(f'     5 - Single VLAN')
                        print(f'     1-10 - Range of VLANs')
                        print(f'     1,2,3,4,5,11,12,13,14,15 - List of VLANs')
                        print(f'     1-10,20-30 - Ranges and Lists of VLANs')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                policy_list = [
                    'policies_vlans.multicast_policies.multicast_policy'
                ]
                templateVars["allow_opt_out"] = False
                for policy in policy_list:
                    policy_short = policy.split('.')[2]
                    templateVars[policy_short],policyData = policy_select_loop(name_prefix, policy, **templateVars)
                    templateVars.update(policyData)

                if not native_vlan == '' and len(vlan_list) > 1:
                    templateVars["vlans"] = [
                        {
                            'auto_allow_on_uplinks':True,
                            'id':native_vlan,
                            'multicast_policy':templateVars["multicast_policy"],
                            'name':native_name,
                            'native_vlan':True
                        },
                        {
                            'auto_allow_on_uplinks':True,
                            'id':vlan_list,
                            'multicast_policy':templateVars["multicast_policy"],
                            'name':vlan_name,
                            'native_vlan':False
                        }
                    ]
                elif not native_vlan == '' and len(vlan_list) == 1:
                    templateVars["vlans"] = [
                        {
                            'auto_allow_on_uplinks':True,
                            'id':native_vlan,
                            'multicast_policy':templateVars["multicast_policy"],
                            'name':native_name,
                            'native_vlan':True
                        }
                    ]
                else:
                    templateVars["vlans"] = [
                        {
                            'auto_allow_on_uplinks':True,
                            'id':vlan_list,
                            'multicast_policy':templateVars["multicast_policy"],
                            'name':vlan_name,
                            'native_vlan':False
                        }
                    ]

                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Do you want to accept the following configuration?')
                print(f'   description      = "{templateVars["descr"]}"')
                print(f'   multicast_policy = "{templateVars["multicast_policy"]}"')
                print(f'   name             = "{templateVars["name"]}"')
                if not native_vlan == '':
                    print(f'   native_vlan      = "{native_vlan}"')
                    print(f'   native_vlan_name = "{native_name}"')
                print(f'   vlan_list        = "{vlan_list}"')
                print(f'   vlan_name        = "{vlan_name}"')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                valid_confirm = False
                while valid_confirm == False:
                    confirm_policy = input('Enter "Y" or "N" [Y]: ')
                    if confirm_policy == 'Y' or confirm_policy == '':
                        confirm_policy = 'Y'

                        # Write Policies to Template File
                        templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                        write_to_template(self, **templateVars)

                        # Add VLANs to VLAN Policy List
                        vlan_policies_vlans.append({templateVars['name']:vlan_list_expanded})

                        configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                        valid_confirm = True

                    elif confirm_policy == 'N':
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Starting {templateVars["policy_type"]} Section over.')
                        print(f'\n------------------------------------------------------\n')
                        valid_confirm = True

                    else:
                        print(f'\n------------------------------------------------------\n')
                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                        print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # VSAN Policy Module
    #========================================
    def vsan_policies(self):
        vsan_policies_vsans = []
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'VSAN Policy'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'vsan_policies'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  You can Skip this policy if you are not configuring Fibre-Channel.\n')
            print(f'  A {policy_type} will define the VSANs Assigned to the Fabric Interconnects.  You will need')
            print(f'  one VSAN Policy for Fabric A and another VSAN Policy for Fabric B.\n')
            print(f'  IMPORTANT Note: The Fabric Interconnects will encapsulate Fibre-Channel traffic locally')
            print(f'                  in a FCoE (Fibre-Channel over Ethernet) VLAN.  This VLAN Must not be')
            print(f'                  already used by the VLAN Policy.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 0
                policy_loop = False
                while policy_loop == False:

                    name = naming_rule_fabric(loop_count, name_prefix, org)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)
                    templateVars["auto_allow_on_uplinks"] = True

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Uplink Trunking: Default is No.')
                    print(f'     Most deployments do not enable Uplink Trunking for Fibre-Channel. ')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        uplink_trunking = input('Do you want to Enable Uplink Trunking for this VSAN Policy? [N]? ')
                        if uplink_trunking == 'Y':
                            templateVars["uplink_trunking"] = True
                            valid = True
                        else:
                            templateVars["uplink_trunking"] = False
                            valid = True

                    templateVars["vsans"] = []
                    vsan_count = 0
                    vsan_loop = False
                    while vsan_loop == False:
                        valid = False
                        while valid == False:
                            if loop_count % 2 == 0:
                                vsan_id = input(f'Enter the VSAN id to add to {templateVars["name"]}. [100]: ')
                            else:
                                vsan_id = input(f'Enter the VSAN id to add to {templateVars["name"]}. [200]: ')
                            if loop_count % 2 == 0 and vsan_id == '':
                                vsan_id = 100
                            elif vsan_id == '':
                                vsan_id = 200
                            if re.search(r'[0-9]{1,4}', str(vsan_id)):
                                valid = validating_ucs.number_in_range('VSAN ID', vsan_id, 1, 4094)
                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Invalid Entry!  Please Enter a VSAN ID in the range of 1-4094.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            fcoe_id = input(f'Enter the VLAN id for the FCOE VLAN to encapsulate "{vsan_id}" over Ethernet.  [{vsan_id}]: ')
                            if fcoe_id == '':
                                fcoe_id = vsan_id
                            if re.search(r'[0-9]{1,4}', str(fcoe_id)):
                                valid_vlan = validating_ucs.number_in_range('VSAN ID', fcoe_id, 1, 4094)
                                if valid_vlan == True:
                                    policy_list = [
                                        'policies_vlans.vlan_policies.vlan_policy',
                                    ]
                                    templateVars["allow_opt_out"] = False
                                    for policy in policy_list:
                                        vlan_policy,policyData = policy_select_loop(name_prefix, policy, **templateVars)
                                    vlan_list = []
                                    for item in policyData['vlan_policies']:
                                        for key, value in item.items():
                                            if key == vlan_policy:
                                                for i in value[0]['vlans']:
                                                    for k, v in i.items():
                                                        for x in v:
                                                            for y, val in x.items():
                                                                if y == 'vlan_list':
                                                                    vlan_list.append(val)

                                    vlan_list = ','.join(vlan_list)
                                    vlan_list = vlan_list_full(vlan_list)
                                    overlap = False
                                    for vlan in vlan_list:
                                        if int(vlan) == int(fcoe_id):
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                            print(f'  Error!!  The FCoE VLAN {fcoe_id} is already assigned to the VLAN Policy')
                                            print(f'  {vlan_policy}.  Please choose a VLAN id that is not already in use.')
                                            print(f'\n-------------------------------------------------------------------------------------------\n')
                                            overlap = True
                                            break
                                    if overlap == False:
                                        valid = True
                                else:
                                    print(f'\n-------------------------------------------------------------------------------------------\n')
                                    print(f'  Invalid Entry!  Please Enter a valid VLAN ID in the range of 1-4094.')
                                    print(f'\n-------------------------------------------------------------------------------------------\n')

                            else:
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Invalid Entry!  Please Enter a valid VLAN ID in the range of 1-4094.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')

                        valid = False
                        while valid == False:
                            if loop_count % 2 == 0:
                                vsan_name = input(f'What Name would you like to assign to "{vsan_id}"?  [VSAN-A]: ')
                            else:
                                vsan_name = input(f'What Name would you like to assign to "{vsan_id}"?  [VSAN-B]: ')
                            if loop_count % 2 == 0 and vsan_name == '':
                                vsan_name = 'VSAN-A'
                            elif vsan_name == '':
                                vsan_name = 'VSAN-B'
                            valid = validating_ucs.name_rule('VSAN Name', vsan_name, 1, 62)

                        vsan = {
                            'fcoe_vlan_id':fcoe_id,
                            'name':vsan_name,
                            'id':vsan_id
                        }
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Do you want to accept the following configuration?')
                        print(f'   fcoe_vlan_id = {fcoe_id}')
                        print(f'   vsan_id      = {vsan_id}')
                        print(f'   vsan_name    = "{vsan_name}"')
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        valid_confirm = False
                        while valid_confirm == False:
                            confirm_vsan = input('Enter "Y" or "N" [Y]: ')
                            if confirm_vsan == 'Y' or confirm_vsan == '':
                                templateVars['vsans'].append(vsan)
                                valid_exit = False
                                while valid_exit == False:
                                    vsan_exit = input(f'Would You like to Configure another VSAN?  Enter "Y" or "N" [N]: ')
                                    if vsan_exit == 'Y':
                                        vsan_count += 1
                                        valid_confirm = True
                                        valid_exit = True
                                    elif vsan_exit == 'N' or vsan_exit == '':
                                        vsan_loop = True
                                        valid_confirm = True
                                        valid_exit = True
                                    else:
                                        print(f'\n------------------------------------------------------\n')
                                        print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                        print(f'\n------------------------------------------------------\n')

                            elif confirm_vsan == 'N':
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                print(f'  Starting VSAN Configuration Over.')
                                print(f'\n-------------------------------------------------------------------------------------------\n')
                                valid_confirm = True
                            else:
                                print(f'\n------------------------------------------------------\n')
                                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                                print(f'\n------------------------------------------------------\n')

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    description     = "{templateVars["descr"]}"')
                    print(f'    name            = "{templateVars["name"]}"')
                    print(f'    uplink_trunking = {templateVars["uplink_trunking"]}')
                    print(f'    vsans           = [')
                    item_count = 1
                    for item in templateVars["vsans"]:
                        print(f'      {item_count} = ''{')
                        for k, v in item.items():
                            if k == 'fcoe_vlan_id':
                                print(f'        fcoe_vlan_id = {v}')
                            elif k == 'name':
                                print(f'        name         = {v}')
                            elif k == 'id':
                                print(f'        vsan_id      = {v}')
                        print('      }')
                        item_count += 1
                    print(f'    ]')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            # Add VSANs to VSAN Policy List
                            vsan_policies_vsans.append({templateVars['name']:templateVars["vsans"]})

                            configure_loop, loop_count, policy_loop = exit_loop_default_yes(loop_count, policy_type)
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {policy_type} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # WWNN Pools Module
    #========================================
    def wwnn_pools(self):
        name_prefix = self.name_prefix
        name_suffix = 'wwnn_pool'
        org = self.org
        policy_type = 'WWNN Pool'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'wwnn_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  WWNN Pool Convention Recommendations:')
            print(f'  - Leverage the Cisco UCS OUI of 20:00:00:25:B5 for the WWNN Pool Prefix.')
            print(f'  - Pool Size can be between 1 and 1000 addresses.')
            print(f'  - Refer to "UCS Naming Conventions 0.5.ppsx" in the Repository for further guidance.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                policy_loop = False
                while policy_loop == False:

                    if not name_prefix == '':
                        name = '%s_%s' % (name_prefix, name_suffix)
                    else:
                        name = '%s_%s' % (org, name_suffix)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the number for the value to select.  [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

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
                    templateVars["wwnn_blocks"] = [{'from':begin, 'to':ending}]

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    assignment_order = "{templateVars["assignment_order"]}"')
                    print(f'    description      = "{templateVars["descr"]}"')
                    print(f'    name             = "{templateVars["name"]}"')
                    print(f'    wwnn_blocks = [')
                    for item in templateVars["wwnn_blocks"]:
                        print('      {')
                        for k, v in item.items():
                            if k == 'from':
                                print(f'        from = "{v}" ')
                            elif k == 'to':
                                print(f'        to   = "{v}"')
                        print('      }')
                    print(f'    ]')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, policy_loop = exit_default_no(templateVars["policy_type"])
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {templateVars["policy_type"]} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n-------------------------------------------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

    #========================================
    # WWPN Pools Module
    #========================================
    def wwpn_pools(self):
        name_prefix = self.name_prefix
        org = self.org
        policy_type = 'WWPN Pool'
        templateVars = {}
        templateVars["header"] = '%s Variables' % (policy_type)
        templateVars["initial_write"] = True
        templateVars["org"] = org
        templateVars["policy_type"] = policy_type
        templateVars["template_file"] = 'template_open.jinja2'
        templateVars["template_type"] = 'wwpn_pools'

        # Open the Template file
        write_to_template(self, **templateVars)
        templateVars["initial_write"] = False

        configure_loop = False
        while configure_loop == False:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  WWPN Pool Convention Recommendations:')
            print(f'  - Leverage the Cisco UCS OUI of 20:00:00:25:B5 for the WWPN Pool Prefix.')
            print(f'  - For WWPN Pools; create a pool for each Fabric.')
            print(f'  - Pool Size can be between 1 and 1000 addresses.')
            print(f'  - Refer to "UCS Naming Conventions 0.5.ppsx" in the Repository for further guidance.\n')
            print(f'  This wizard will save the configuraton for this section to the following file:')
            print(f'  - Intersight/{org}/{self.type}/{templateVars["template_type"]}.auto.tfvars')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            configure = input(f'Do You Want to Configure a {policy_type}?  Enter "Y" or "N" [Y]: ')
            if configure == 'Y' or configure == '':
                loop_count = 0
                policy_loop = False
                while policy_loop == False:

                    name = naming_rule_fabric(loop_count, name_prefix, org)

                    templateVars["name"] = policy_name(name, policy_type)
                    templateVars["descr"] = policy_descr(templateVars["name"], policy_type)

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Assignment order decides the order in which the next identifier is allocated.')
                    print(f'    1. default - (Intersight Default) Assignment order is decided by the system.')
                    print(f'    2. sequential - (Recommended) Identifiers are assigned in a sequential order.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid = False
                    while valid == False:
                        templateVars["assignment_order"] = input('Specify the number for the value to select.  [2]: ')
                        if templateVars["assignment_order"] == '' or templateVars["assignment_order"] == '2':
                            templateVars["assignment_order"] = 'sequential'
                            valid = True
                        elif templateVars["assignment_order"] == '1':
                            templateVars["assignment_order"] = 'default'
                            valid = True
                        else:
                            print(f'\n-------------------------------------------------------------------------------------------\n')
                            print(f'  Error!! Invalid Option.  Please Select a valid option from the List.')
                            print(f'\n-------------------------------------------------------------------------------------------\n')

                    valid = False
                    while valid == False:
                        if loop_count % 2 == 0:
                            begin = input('What is the Beginning WWPN Address to Assign to the Pool?  [20:00:00:25:B5:0A:00:00]: ')
                        else:
                            begin = input('What is the Beginning WWPN Address to Assign to the Pool?  [20:00:00:25:B5:0B:00:00]: ')
                        if begin == '':
                            if loop_count % 2 == 0:
                                begin = '20:00:00:25:B5:0A:00:00'
                            else:
                                begin = '20:00:00:25:B5:0B:00:00'
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
                    templateVars["wwpn_blocks"] = [{'from':begin, 'to':ending}]

                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Do you want to accept the following configuration?')
                    print(f'    assignment_order = "{templateVars["assignment_order"]}"')
                    print(f'    description      = "{templateVars["descr"]}"')
                    print(f'    name             = "{templateVars["name"]}"')
                    print(f'    wwpn_blocks = [')
                    for item in templateVars["wwpn_blocks"]:
                        print('      {')
                        for k, v in item.items():
                            if k == 'from':
                                print(f'        from = "{v}" ')
                            elif k == 'to':
                                print(f'        to   = "{v}"')
                        print('      }')
                    print(f'    ]')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    valid_confirm = False
                    while valid_confirm == False:
                        confirm_policy = input('Enter "Y" or "N" [Y]: ')
                        if confirm_policy == 'Y' or confirm_policy == '':
                            confirm_policy = 'Y'

                            # Write Policies to Template File
                            templateVars["template_file"] = '%s.jinja2' % (templateVars["template_type"])
                            write_to_template(self, **templateVars)

                            configure_loop, loop_count, policy_loop = exit_loop_default_yes(loop_count, policy_type)
                            valid_confirm = True

                        elif confirm_policy == 'N':
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Starting {policy_type} Section over.')
                            print(f'\n------------------------------------------------------\n')
                            valid_confirm = True

                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')

            elif configure == 'N':
                configure_loop = True
            else:
                print(f'\n------------------------------------------------------\n')
                print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                print(f'\n------------------------------------------------------\n')

        # Close the Template file
        templateVars["template_file"] = 'template_close.jinja2'
        write_to_template(self, **templateVars)

def choose_policy(policy, **templateVars):

    if 'policies' in policy:
        policy_short = policy.replace('policies', 'policy')
    elif 'pools' in policy:
        policy_short = policy.replace('pools', 'pool')
    x = policy_short.split('_')
    policy_description = []
    for y in x:
        y = y.capitalize()
        policy_description.append(y)
    policy_description = " ".join(policy_description)
    policy_description = policy_description.replace('Ip', 'IP')
    policy_description = policy_description.replace('Ntp', 'NTP')
    policy_description = policy_description.replace('Snmp', 'SNMP')
    policy_description = policy_description.replace('Wwnn', 'WWNN')
    policy_description = policy_description.replace('Wwpn', 'WWPN')

    if len(policy) > 0:
        templateVars["policy"] = policy_description
        policy_short = policies_list(templateVars["policies"], **templateVars)
    else:
        policy_short = ""
    return policy_short

def exit_default_no(policy_type):
    valid_exit = False
    while valid_exit == False:
        exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
        if exit_answer == '' or exit_answer == 'N':
            policy_loop = True
            configure_loop = True
            valid_exit = True
        elif exit_answer == 'Y':
            policy_loop = False
            configure_loop = False
            valid_exit = True
        else:
            print(f'\n------------------------------------------------------\n')
            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
            print(f'\n------------------------------------------------------\n')
    return configure_loop, policy_loop

def exit_default_yes(policy_type):
    valid_exit = False
    while valid_exit == False:
        exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
        if exit_answer == '' or exit_answer == 'Y':
            policy_loop = False
            configure_loop = False
            valid_exit = True
        elif exit_answer == 'N':
            policy_loop = True
            configure_loop = True
            valid_exit = True
        else:
            print(f'\n------------------------------------------------------\n')
            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
            print(f'\n------------------------------------------------------\n')
    return configure_loop, policy_loop

def exit_loop_default_yes(loop_count, policy_type):
    valid_exit = False
    while valid_exit == False:
        if loop_count % 2 == 0:
            exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [Y]: ')
        else:
            exit_answer = input(f'Would You like to Configure another {policy_type}?  Enter "Y" or "N" [N]: ')
        if (loop_count % 2 == 0 and exit_answer == '') or exit_answer == 'Y':
            policy_loop = False
            configure_loop = False
            loop_count += 1
            valid_exit = True
        elif not loop_count % 2 == 0 and exit_answer == '':
            policy_loop = True
            configure_loop = True
            valid_exit = True
        elif exit_answer == 'N':
            policy_loop = True
            configure_loop = True
            valid_exit = True
        else:
            print(f'\n------------------------------------------------------\n')
            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
            print(f'\n------------------------------------------------------\n')
    return configure_loop, loop_count, policy_loop

def naming_rule(name_prefix, name_suffix, org):
    if not name_prefix == '':
        name = '%s_%s' % (name_prefix, name_suffix)
    else:
        name = '%s_%s' % (org, name_suffix)
    return name

def naming_rule_fabric(loop_count, name_prefix, org):
    if loop_count % 2 == 0:
        if not name_prefix == '':
            name = '%s_A' % (name_prefix)
        elif not org == 'default':
            name = '%s_A' % (org)
        else:
            name = 'Fabric_A'
    else:
        if not name_prefix == '':
            name = '%s_B' % (name_prefix)
        elif not org == 'default':
            name = '%s_B' % (org)
        else:
            name = 'Fabric_B'
    return name

def policies_list(policies_list, **templateVars):
    valid = False
    while valid == False:
        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'  {templateVars["policy"]} Options:')
        for i, v in enumerate(policies_list):
            i += 1
            if i < 10:
                print(f'     {i}. {v}')
            else:
                print(f'    {i}. {v}')
        if templateVars["allow_opt_out"] == True:
            print(f'     99. Do not assign a(n) {templateVars["policy"]}.')
        print(f'     100. Create a New {templateVars["policy"]}.')
        print(f'\n-------------------------------------------------------------------------------------------\n')
        policy_temp = input(f'Select the Option Number for the {templateVars["policy"]} to Assign to {templateVars["name"]}: ')
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
            elif int(policy_temp) == 100:
                policy = 'create_policy'
                valid = True
                return policy

        if policy_temp == '':
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
        elif int(policy_temp) == 99:
            policy = ''
            valid = True
            return policy
        elif int(policy_temp) == 100:
            policy = 'create_policy'
            valid = True
            return policy

def policies_parse(org, policy_type, policy):
    policies = []
    policy_file = './Intersight/%s/%s/%s.auto.tfvars' % (org, policy_type, policy)
    if os.path.isfile(policy_file):
        if len(policy_file) > 0:
            cmd = 'json2hcl -reverse < %s' % (policy_file)
            p = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            if 'unable to parse' in p.stdout.decode('utf-8'):
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  !!!! Encountered Error in Attempting to read file !!!!')
                print(f'  - {policy_file}')
                print(f'  Error was:')
                print(f'  - {p.stdout.decode("utf-8")}')
                print(f'\n-------------------------------------------------------------------------------------------\n')
                jsonData = {}
                return policies,jsonData
            else:
                jsonData = json.loads(p.stdout.decode('utf-8'))
                for i in jsonData[policy]:
                    for k, v in i.items():
                        policies.append(k)
                return policies,jsonData
    else:
        jsonData = {}
        return policies,jsonData

def policy_loop_standard(self, header, initial_policy, template_type):
    # Set the org_count to 0 for the First Organization
    org_count = 0

    # Loop through the orgs discovered by the Class
    for org in self.orgs:

        # Pull in Variables from Class
        templateVars = self.templateVars
        templateVars["org"] = org

        # Define the Template Source
        templateVars["header"] = header
        templateVars["template_type"] = template_type
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

        if template_type in self.json_data["config"]["orgs"][org_count]:
            for item in self.json_data["config"]["orgs"][org_count][template_type]:
                # Reset TemplateVars to Default for each Loop
                templateVars = {}
                templateVars["org"] = org

                # Define the Template Source
                templateVars["header"] = header

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

def policy_select_loop(name_prefix, policy, **templateVars):
    valid = False
    while valid == False:
        create_policy = True
        inner_policy = policy.split('.')[1]
        inner_type = policy.split('.')[0]
        inner_var = policy.split('.')[2]
        templateVars[inner_var] = ''
        templateVars["policies"],policyData = policies_parse(templateVars["org"], inner_type, inner_policy)
        if not len(templateVars['policies']) > 0:
            create_policy = True
        else:
            templateVars[inner_var] = choose_policy(inner_policy, **templateVars)
        if templateVars[inner_var] == 'create_policy':
            create_policy = True
        elif templateVars[inner_var] == '' and templateVars["allow_opt_out"] == True:
            valid = True
            create_policy = False
            return templateVars[inner_var],policyData
        elif not templateVars[inner_var] == '':
            valid = True
            create_policy = False
            return templateVars[inner_var],policyData
        if create_policy == True:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  Starting module to create {inner_policy}')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            if inner_policy == 'ip_pools':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ip_pools()
            elif inner_policy == 'iqn_pools':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).iqn_pools()
            elif inner_policy == 'mac_pools':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).mac_pools()
            elif inner_policy == 'uuid_pools':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).uuid_pools()
            elif inner_policy == 'wwnn_pools':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).wwnn_pools()
            elif inner_policy == 'wwpn_pools':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).wwpn_pools()
            elif inner_policy == 'adapter_configuration_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).adapter_configuration_policies()
            elif inner_policy == 'bios_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).bios_policies()
            elif inner_policy == 'boot_order_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).boot_order_policies()
            elif inner_policy == 'certificate_management_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).certificate_management_policies()
            elif inner_policy == 'device_connector_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).device_connector_policies()
            elif inner_policy == 'ethernet_adapter_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ethernet_adapter_policies()
            elif inner_policy == 'ethernet_network_control_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ethernet_network_control_policies()
            elif inner_policy == 'ethernet_network_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ethernet_network_policies()
            elif inner_policy == 'ethernet_qos_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ethernet_qos_policies()
            elif inner_policy == 'fibre_channel_adapter_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).fibre_channel_adapter_policies()
            elif inner_policy == 'fibre_channel_network_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).fibre_channel_network_policies()
            elif inner_policy == 'fibre_channel_qos_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).fibre_channel_qos_policies()
            elif inner_policy == 'flow_control_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).flow_control_policies()
            elif inner_policy == 'imc_access_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).imc_access_policies()
            elif inner_policy == 'ipmi_over_lan_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ipmi_over_lan_policies()
            elif inner_policy == 'iscsi_adapter_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).iscsi_adapter_policies()
            elif inner_policy == 'iscsi_boot_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).iscsi_boot_policies()
            elif inner_policy == 'iscsi_static_target_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).iscsi_static_target_policies()
            elif inner_policy == 'lan_connectivity_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).lan_connectivity_policies()
            elif inner_policy == 'ldap_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ldap_policies()
            elif inner_policy == 'link_aggregation_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).link_aggregation_policies()
            elif inner_policy == 'link_control_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).link_control_policies()
            elif inner_policy == 'local_user_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).local_user_policies()
            elif inner_policy == 'multicast_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).multicast_policies()
            elif inner_policy == 'network_connectivity_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).network_connectivity_policies()
            elif inner_policy == 'ntp_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ntp_policies()
            elif inner_policy == 'persistent_memory_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).persistent_memory_policies()
            elif inner_policy == 'port_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).port_policies()
            elif inner_policy == 'san_connectivity_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).san_connectivity_policies()
            elif inner_policy == 'sd_card_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).sd_card_policies()
            elif inner_policy == 'serial_over_lan_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).serial_over_lan_policies()
            elif inner_policy == 'smtp_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).smtp_policies()
            elif inner_policy == 'snmp_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).snmp_policies()
            elif inner_policy == 'ssh_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).ssh_policies()
            elif inner_policy == 'storage_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).storage_policies()
            elif inner_policy == 'switch_control_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).switch_control_policies()
            elif inner_policy == 'syslog_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).syslog_policies()
            elif inner_policy == 'system_qos_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).system_qos_policies()
            elif inner_policy == 'thermal_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).thermal_policies()
            elif inner_policy == 'virtual_kvm_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).virtual_kvm_policies()
            elif inner_policy == 'virtual_media_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).virtual_media_policies()
            elif inner_policy == 'vlan_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).vlan_policies()
            elif inner_policy == 'vsan_policies':
                easy_imm_wizard(name_prefix, templateVars["org"], inner_type).vsan_policies()

def policy_descr(name, policy_type):
    valid = False
    while valid == False:
        descr = input(f'What is the Description for the {policy_type}?  [{name} {policy_type}]: ')
        if descr == '':
            descr = '%s %s' % (name, policy_type)
        valid = validating_ucs.description(f'{policy_type} Description', descr, 1, 62)
        if valid == True:
            return descr

def policy_name(namex, policy_type):
    valid = False
    while valid == False:
        name = input(f'What is the Name for the {policy_type}?  [{namex}]: ')
        if name == '':
            name = '%s' % (namex)
        valid = validating_ucs.name_rule(f'{policy_type} Name', name, 1, 62)
        if valid == True:
            return name

def policy_template(self, **templateVars):
    configure_loop = False
    while configure_loop == False:
        policy_loop = False
        while policy_loop == False:

            valid = False
            while valid == False:
                policy_file = 'ucs_templates/variables/%s' % (templateVars["policy_file"])
                if os.path.isfile(policy_file):
                    template_file = open(policy_file, 'r')
                    template_file.seek(0)
                    policy_templates = []
                    for line in template_file:
                        line = line.strip()
                        policy_templates.append(line)
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  {templateVars["policy_type"]} Templates:')
                    for i, v in enumerate(policy_templates):
                        i += 1
                        if i < 10:
                            print(f'     {i}. {v}')
                        else:
                            print(f'    {i}. {v}')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                policy_temp = input(f'Enter the Index Number for the {templateVars["policy_type"]} Template to Create: ')
                for i, v in enumerate(policy_templates):
                    i += 1
                    if int(policy_temp) == i:
                        templateVars["policy_template"] = v
                        valid = True
                if valid == False:
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Error!! Invalid Selection.  Please Select a valid Index from the List.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                template_file.close()

            if not templateVars["name_prefix"] == '':
                name = '%s_%s' % (templateVars["name_prefix"], templateVars["policy_template"])
            else:
                name = '%s_%s' % (templateVars["org"], templateVars["policy_template"])

            templateVars["name"] = policy_name(name, templateVars["policy_type"])
            templateVars["descr"] = policy_descr(templateVars["name"], templateVars["policy_type"])

            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  Do you want to accept the following configuration?')
            if templateVars["template_type"] == 'bios_policies':
                print(f'   bios_template = "{templateVars["policy_template"]}"')
                print(f'   description   = "{templateVars["descr"]}"')
                print(f'   name          = "{templateVars["name"]}"')
            else:
                print(f'   adapter_template = "{templateVars["policy_template"]}"')
                print(f'   description      = "{templateVars["descr"]}"')
                print(f'   name             = "{templateVars["name"]}"')
            print(f'\n-------------------------------------------------------------------------------------------\n')
            valid_confirm = False
            while valid_confirm == False:
                confirm_policy = input('Enter "Y" or "N" [Y]: ')
                if confirm_policy == 'Y' or confirm_policy == '':
                    confirm_policy = 'Y'

                    # Write Policies to Template File
                    write_to_template(self, **templateVars)

                    configure_loop, policy_loop = exit_default_yes(templateVars["policy_type"])
                    valid_confirm = True

                elif confirm_policy == 'N':
                    print(f'\n------------------------------------------------------\n')
                    print(f'  Starting {templateVars["policy_type"]} Section over.')
                    print(f'\n------------------------------------------------------\n')
                    valid_confirm = True

                else:
                    print(f'\n------------------------------------------------------\n')
                    print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                    print(f'\n------------------------------------------------------\n')

def vars_from_list(var_options, **templateVars):
    selection = []
    selection_count = 0
    valid = False
    while valid == False:
        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'{templateVars["var_description"]}')
        for index, value in enumerate(var_options):
            index += 1
            if index < 10:
                print(f'     {index}. {value}')
            else:
                print(f'    {index}. {value}')
        print(f'\n-------------------------------------------------------------------------------------------\n')
        exit_answer = False
        while exit_answer == False:
            var_selection = input(f'Please Enter the Option Number to Select for {templateVars["var_type"]}: ')
            if not var_selection == '':
                if re.search(r'[0-9]+', str(var_selection)):
                    xcount = 1
                    for index, value in enumerate(var_options):
                        index += 1
                        if int(var_selection) == index:
                            selection.append(value)
                            xcount = 0
                    if xcount == 0:
                        if selection_count % 2 == 0 and templateVars["multi_select"] == True:
                            answer_finished = input(f'Would you like to add another port to the {templateVars["port_type"]}?  Enter "Y" or "N" [Y]: ')
                        elif templateVars["multi_select"] == True:
                            answer_finished = input(f'Would you like to add another port to the {templateVars["port_type"]}?  Enter "Y" or "N" [N]: ')
                        elif templateVars["multi_select"] == False:
                            answer_finished = 'N'
                        if (selection_count % 2 == 0 and answer_finished == '') or answer_finished == 'Y':
                            exit_answer = True
                            selection_count += 1
                        elif answer_finished == '' or answer_finished == 'N':
                            exit_answer = True
                            valid = True
                        elif templateVars["multi_select"] == False:
                            exit_answer = True
                            valid = True
                        else:
                            print(f'\n------------------------------------------------------\n')
                            print(f'  Error!! Invalid Value.  Please enter "Y" or "N".')
                            print(f'\n------------------------------------------------------\n')
                    else:
                        print(f'\n-------------------------------------------------------------------------------------------\n')
                        print(f'  Error!! Invalid Selection.  Please select a valid option from the List.')
                        print(f'\n-------------------------------------------------------------------------------------------\n')

                else:
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  Error!! Invalid Selection.  Please Select a valid Option from the List.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Selection.  Please Select a valid Option from the List.')
                print(f'\n-------------------------------------------------------------------------------------------\n')
    return selection

def process_method(wr_method, dest_dir, dest_file, template, **templateVars):
    dest_dir = './Intersight/%s/%s' % (templateVars["org"], dest_dir)
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
        print(f'\n-------------------------------------------------------------------------------------------\n')
        print(f'{templateVars["var_description"]}')
        policy_file = 'ucs_templates/variables/%s' % (templateVars["policy_file"])
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
        print(f'\n-------------------------------------------------------------------------------------------\n')
        var_selection = input(f'Please Enter the Option Number to Select for {templateVars["var_type"]}: ')
        if not var_selection == '':
            if templateVars["multi_select"] == False and re.search(r'^[0-9]+$', str(var_selection)):
                for index, value in enumerate(varsx):
                    index += 1
                    if int(var_selection) == index:
                        selection = value
                        valid = True
            elif templateVars["multi_select"] == True and re.search(r'(^[0-9]+$|^[0-9\-,]+[0-9]$)', str(var_selection)):
                var_list = vlan_list_full(var_selection)
                var_length = int(len(var_list))
                var_count = 0
                selection = []
                for index, value in enumerate(varsx):
                    index += 1
                    for vars in var_list:
                        if int(vars) == index:
                            var_count += 1
                            selection.append(value)
                if var_count == var_length:
                    valid = True
                else:
                    print(f'\n-------------------------------------------------------------------------------------------\n')
                    print(f'  The list of Vars {var_list} did not match the available list.')
                    print(f'\n-------------------------------------------------------------------------------------------\n')
            else:
                print(f'\n-------------------------------------------------------------------------------------------\n')
                print(f'  Error!! Invalid Selection.  Please Select a valid Option from the List.')
                print(f'\n-------------------------------------------------------------------------------------------\n')
        else:
            print(f'\n-------------------------------------------------------------------------------------------\n')
            print(f'  Error!! Invalid Selection.  Please Select a valid Option from the List.')
            print(f'\n-------------------------------------------------------------------------------------------\n')
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
    template = self.templateEnv.get_template(templateVars["template_file"])

    # Process the template
    dest_dir = '%s' % (self.type)
    dest_file = '%s.auto.tfvars' % (templateVars["template_type"])
    if templateVars["initial_write"] == True:
        write_method = 'w'
    else:
        write_method = 'a'
    process_method(write_method, dest_dir, dest_file, template, **templateVars)
