def get_visited_post(request, pk):
    context = {
        'flag': False,
        'value':request.GET.get('visited_post'),
        }
    if context.get('value'):
        view_list = context.get('value').split('_')
        if str(pk) not in view_list:
            context['value'] += f'_{pk}'
            context['flag'] = True
    else:
        context['value'] = pk
        context['flag'] = True

    return context