Introduction
============

``collective.jekyll`` is a Plone add-on to help users diagnose the state of
their content.

.. contents:: Table of contents

Overview
========


Symptoms
========


Adding more symptoms
====================


Disabling existing symptoms
===========================

You can disable symptom(s) by adding ``registry.xml`` step in your product
GenericSetup profile. 

Here is an sample ``registry.xml`` to disable IdFormatSymptom symptom::

    <registry>

        <record name="collective.jekyll.symptoms.IdFormatSymptom">
            <field type="plone.registry.field.Bool">
                <title>Id Format Symptom</title>
                <description>Define if Id Format Symptom is active</description>
            </field>
            <value>False</value>
        </record>

    </registry>
