import os
import tempfile
from django.shortcuts import render,get_object_or_404
from django.http import FileResponse, HttpResponseBadRequest
import yt_dlp
from django_ratelimit.decorators import ratelimit
from .models import DownloadTicket
import tempfile

@ratelimit(key='ip', rate='7/m', block=True)
def index(request):
    if request.method == "POST":
        video_url = request.POST.get("video_url")
        
        if not video_url:
            return HttpResponseBadRequest("Please provide a valid YouTube link.")
            

        temp_dir = tempfile.gettempdir()
        output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")
        
        ydl_opts = {
            'format': 'best', 
            'outtmpl': output_template,
            'noplaylist': True,
        }
        


    return render(request, "index.html")

def process_ticket_download(request, ticket_id):
    ticket = get_object_or_404(DownloadTicket, id=ticket_id, user=request.user)
  
    video_url = ticket.video_url
    

    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)
        
    response_file = open(filename, 'rb')
    return FileResponse(response_file, as_attachment=True, filename=os.path.basename(filename))