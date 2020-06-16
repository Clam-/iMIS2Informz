MAILINGS = """<Grid type="mailing">
<ReturnFields>
<DataElement>accounting_code</DataElement>
<DataElement>create_date</DataElement>
<DataElement>folder_id</DataElement>
<DataElement>folder_name</DataElement>
<DataElement>friendly_from</DataElement>
<DataElement>from_address</DataElement>
<DataElement>is_deleted</DataElement>
<DataElement>last_sent_date</DataElement>
<DataElement>mailing_id</DataElement>
<DataElement>modify_date</DataElement>
<DataElement>modify_email</DataElement>
<DataElement>modify_user_id</DataElement>
<DataElement>name</DataElement>
<DataElement>reply_to</DataElement>
<DataElement>schedule_choice</DataElement>
<DataElement>send_at_date</DataElement>
<DataElement>subject</DataElement>
<DataElement>template_id</DataElement>
<DataElement>template_name</DataElement>
</ReturnFields>
</Grid>"""

OLDBODY = """<Grid type="subscriber">
<ReturnFields>
<DataElement>bounce_date</DataElement>
<DataElement>cancellation_mailing_instance_id</DataElement>
<DataElement>cancellation_message</DataElement>
<DataElement>cancellation_date</DataElement>
<DataElement>email</DataElement>
<DataElement>is_repeated_bouncer</DataElement>
<DataElement>is_unsubscriber</DataElement>
<DataElement>modified_date</DataElement>
<DataElement>service_since_date</DataElement>
<DataElement>user_id</DataElement>
<DataElement>subscriber_upload_id</DataElement>
<DataElement>imis_name_id</DataElement>
</ReturnFields>
</Grid>""".replace("\n", "")

INTERESTS = """<Grid type="subscriber_interests">
   <ReturnFields>
    <DataElement>cancellation_date</DataElement>
    <DataElement>cancelled_id</DataElement>
    <DataElement>email</DataElement>
    <DataElement>interest_id</DataElement>
    <DataElement>interest_name</DataElement>
    <DataElement>service_since_date</DataElement>
    <DataElement>subscriber_to_interest_id</DataElement>
   </ReturnFields>
  </Grid>"""
