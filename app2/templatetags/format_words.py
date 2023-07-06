from django import template

register = template.Library()

@register.filter
def get_class_day(value):
	return value.class_day

@register.filter
def format_gender(value):
	if value == 'female':
		return 'Feminino'
	if value == 'male':
		return 'Masculino'


@register.filter
def get_first_letter(value):
	return value[0].upper()

@register.filter
def capitalize(value):
	return value.title()

@register.filter
def format_test(value):
	value = value.split('st')
	value = value[0].title() + 'st' + value[-1]
	return value

@register.filter
def capitalize(value):
	return value.title()





