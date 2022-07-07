import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest

from pagination.models import Text


class Pagination:
    def __init__(self,
                 limit: int,
                 model_class: 'Models'):
        self.limit = limit
        self.model_class = model_class

    def _split_result(self):
        try:
            # This part of code may be separated, but it was inserted to not expand too much the code.
            # In a prod environment I'd use a kind of serializer to make this scalable for others models.
            # --------------------------------------------------------------------------------------
            list_and_serialize_results = [
                {
                    "id": i.id,
                    "description": i.description
                } for i in self.model_class.objects.order_by('-id')
            ]
            # --------------------------------------------------------------------------------------
            for i in range(0, len(list_and_serialize_results), self.limit):
                yield list_and_serialize_results[i:i + self.limit]
        except Exception as e:
            raise e

    def num_of_pages(self):
        try:
            num = int(self.model_class.objects.count() / self.limit)
            if num == 0:
                return 1
            else:
                return num
        except Exception as e:
            raise e

    def result(self, number_of_page_choosen: int):
        try:
            number_of_page_choosen = number_of_page_choosen - 1
            return list(self._split_result())[number_of_page_choosen]
        except Exception as e:
            raise e


def pagination_buttons(page_choosen: int, array_of_pages: list):

    def clear_list(list_):
        clear = []
        for i in list_:
            if i not in clear:
                clear.append(i)
        return clear

    page_choosen = page_choosen - 1
    if page_choosen == 0 and max(array_of_pages) > 10:
        return clear_list([
            array_of_pages[0],
            array_of_pages[1],
            array_of_pages[2],
            "...",
            array_of_pages[-2],
            array_of_pages[-1]
        ])
    if page_choosen + 1 == max(array_of_pages) and max(array_of_pages) > 10:
        return clear_list([
            array_of_pages[0],
            array_of_pages[1],
            "...",
            array_of_pages[-3],
            array_of_pages[-2],
            array_of_pages[-1]
        ])
    if max(array_of_pages) >= 10:
        return [
            array_of_pages[0],
            array_of_pages[1],
            "...",
            array_of_pages[page_choosen - 1],
            array_of_pages[page_choosen],
            array_of_pages[page_choosen + 1],
            "...",
            array_of_pages[-2],
            array_of_pages[-1]
        ]
    else:
        if max(array_of_pages) < 10:
            return [i for i in range(1, max(array_of_pages))]


def pagination_text(request):
    try:
        page = int(request.GET.get("page", None))
        limit = int(request.GET.get("limit", None))
        data = Pagination(limit=limit, model_class=Text)
        data = {
            "success": True,
            "data": data.result(number_of_page_choosen=page),
            "array_of_pages": pagination_buttons(page_choosen=page,
                                                 array_of_pages=[i for i in range(data.num_of_pages())])
        }
        return render(request, "pagination.html", {"data": data})
    except Exception as e:
        return HttpResponseBadRequest(str(e))  # Not a good practice, only for browser's tests purpose
