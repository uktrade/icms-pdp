import django.forms.widgets as widgets


class DateInput(widgets.DateInput):
    template_name = "forms/widgets/date.html"


#  class Textarea(Textarea):
#      template_name = 'forms/widgets/textarea.html'

#  class EmailInput(EmailInput):
#      template_name = 'forms/widgets/input.html'

#  class Select(Select):
#      template_name = 'forms/widgets/select.html'

#  class Display(TextInput):
#      """ Widget to display the field as text"""
#    template_name = 'forms/widgets/input.html'

#  class Hiddennput(HiddenInput):
#      pass

#  class CheckboxInput(CheckboxInput):
#      pass
