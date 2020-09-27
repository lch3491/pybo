from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm


def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)
    
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)    
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
    
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)    

def question_create(request): 
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)    

    
    
"""    
generic view 사용 시 

class IndexView(generic.ListView): 
    def get_queryset(self): 
        return Question.objects.order_by('-create_date') 
        
class DetailView(generic.DetailView): 
    model = Question
    
 -- urls.py --
urlpatterns = [ 
    path('', views.IndexView.as_view()), 
    path('<int:pk>/', views.DetailView.as_view()), 
]
"""