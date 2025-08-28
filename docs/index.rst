
Welcome to Shepherd's DevLog!
=============================================

Main-Documentation: https://nes-lab.github.io/shepherd

Source to this DevLog: https://github.com/orgua/shepherd-v2-planning

.. Note::
   The included search-function is often able to find the needle in the haystack (especially in the overwhelming dev-log)


.. toctree::
   :maxdepth: 2
   :caption: Overview

   00_overview/requirements_2020
   00_overview/feasibility_2020

   00_overview/concept_shepherd
   00_overview/concept_testbed
   00_overview/concept_tu_dresden

   00_overview/requirement_refinement_2022

   00_overview/comparison_other_testbeds
   00_overview/learnings_other_testbeds
   00_overview/flocklab_inheritance

.. toctree::
   :maxdepth: 2
   :caption: Cape

   10_capes/concept_capes
   10_capes/concept_cad

   10_capes/test_for_functionality

   10_capes/cape_v20_design
   10_capes/cape_v20_performance
   10_capes/cape_v21_design
   10_capes/cape_v21_performance
   10_capes/cape_v22_design
   10_capes/cape_v22_performance
   10_capes/cape_v23_design
   10_capes/cape_v23_performance
   10_capes/cape_v24_design
   10_capes/cape_v24_performance
   10_capes/cape_v24_measurements
   10_capes/cape_v25_design
   10_capes/cape_v26_design

.. toctree::
   :maxdepth: 2
   :caption: Targets

   20_targets/nRF52_FRAM_concept
   20_targets/target_v23_design

.. toctree::
   :maxdepth: 2
   :caption: HW Components & Debugging

   30_components_debugging/beaglebone_boot_pins
   30_components_debugging/watchdog
   30_components_debugging/lsf_level_translator_v22/README
   30_components_debugging/noise_performance/README
   30_components_debugging/target_voltage
   30_components_debugging/recorder_drain
   30_components_debugging/cape_v24_emu_noise_improvements

   30_components_debugging/harvester_validation_v23/README

   30_components_debugging/programming_interface_improvements

.. toctree::
   :maxdepth: 2
   :caption: Observer & Embedded Sys

   40_embedded_sys/concept_pru
   40_embedded_sys/concept_py

   40_embedded_sys/concept_casing

   40_embedded_sys/initialize_sys_manually

   40_embedded_sys/improve_linux
   40_embedded_sys/improve_security
   40_embedded_sys/improve_py_upgrade
   40_embedded_sys/fix_device_tree
   40_embedded_sys/ubuntu_2204_migration

   40_embedded_sys/crypto_module

   40_embedded_sys/evaluate_beaglebone_AI
   40_embedded_sys/evaluate_beaglebone_AI64
   40_embedded_sys/evaluate_raspberry_CM4

   40_embedded_sys/legacy_branch_backports

.. toctree::
   :maxdepth: 2
   :caption: SW Components & Debugging

   50_sw_debugging/virtual_source_regulator/README

   50_sw_debugging/improve_pru
   50_sw_debugging/h5py_memoryleak
   50_sw_debugging/usb_thumbdrive_trouble
   50_sw_debugging/python_optimization/README
   50_sw_debugging/kernel_panics

.. toctree::
   :maxdepth: 2
   :caption: Server

   60_server/requirements

   60_server/config_basics
   60_server/config_icmp
   60_server/config_rpc_portmapper
   60_server/config_sshd
   60_server/config_ssl_certificates

.. toctree::
   :maxdepth: 2
   :caption: Network

   70_network/requirements

   70_network/timesync_gpio_level_pru/README
   70_network/timesync_tune_ptp
   70_network/timesync_dedicated_ptp_switch
   70_network/timesync_revisited


.. toctree::
   :maxdepth: 2
   :caption: Web

   80_web/concept_web

.. toctree::
   :maxdepth: 2
   :caption: Student Projects

   90_student_projects/introduction
   90_student_projects/implement_dataviewer
   90_student_projects/improvement_for_memory_interface


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
