from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

posts = [
    {
        "slug": "serene-woods",
        "image": "woods.jpg",
        "author": "Touhidul Islam",
        "date": date(2026, 7, 21),
        "title": "The Calm of the Deep Woods",
        "excerpt": "Step away from the city noise and immerse yourself in the peaceful symphony of rustling leaves and ancient woodland trails.",
        "content": """
        The deep woods have a magical way of slowing down time. Sunlight filters through the dense canopy of emerald leaves, casting dappled patterns on the mossy forest floor. Walking among these giants reminds us of the resilience of nature and provides the perfect refuge for quiet reflection and rejuvenation.
         The deep woods have a magical way of slowing down time. Sunlight filters through the dense canopy of emerald leaves, casting dappled patterns on the mossy forest floor. Walking among these giants reminds us of the resilience of nature and provides the perfect refuge for quiet reflection and rejuvenation.
          The deep woods have a magical way of slowing down time. Sunlight filters through the dense canopy of emerald leaves, casting dappled patterns on the mossy forest floor. Walking among these giants reminds us of the resilience of nature and provides the perfect refuge for quiet reflection and rejuvenation.
        """
    },
    {
        "slug": "river-valley-journey",
        "image": "river.jpg",
        "author": "Sarah Jenkins",
        "date": date(2026, 7, 16),
        "title": "A Journey Through the River Valley",
        "excerpt": "Follow the winding currents of crystal-clear mountain rivers as they carve through lush valleys and rocky gorges.",
        "content": """
        Rivers are the lifelines of the wilderness, nourishing rich ecosystems along their banks. From gentle freshwater streams to thundering rapids, exploring a river valley reveals hidden coves, smooth river stones, and abundant wildlife thriving near the water's edge.
        Rivers are the lifelines of the wilderness, nourishing rich ecosystems along their banks. From gentle freshwater streams to thundering rapids, exploring a river valley reveals hidden coves, smooth river stones, and abundant wildlife thriving near the water's edge.
        """
    },
    {
        "slug": "grand-canyon-adventure",
        "image": "canyon.jpg",
        "author": "Alex Rivera",
        "date": date(2026, 7, 11),
        "title": "The Grandeur of Desert Canyons",
        "excerpt": "Discover the dramatic red rock formations and ancient geological storytelling etched into towering canyon walls.",
        "content": """
        Carved over millions of years by wind and water, canyon landscapes offer some of the most dramatic scenery on Earth. As the sun sets, the rock faces ignite in fiery shades of crimson, orange, and gold, creating an unforgettable desert spectacle.
        
        
        
        Carved over millions of years by wind and water, canyon landscapes offer some of the most dramatic scenery on Earth. As the sun sets, the rock faces ignite in fiery shades of crimson, orange, and gold, creating an unforgettable desert spectacle.
        """
    },
    {
        "slug": "misty-forest-walk",
        "image": "forest.jpg",
        "author": "Touhidul Islam",
        "date": date(2026, 7, 6),
        "title": "Whispers in the Misty Forest",
        "excerpt": "Wander through enchanted foggy trails where towering trees disappear into mist and silence reigns supreme.",
        "content": """
        A morning fog transforms an ordinary woodland walk into an atmospheric adventure. The cool mist hugs the trees, muting ambient sounds and creating a mystical solitude that feels worlds away from everyday life.
         A morning fog transforms an ordinary woodland walk into an atmospheric adventure. The cool mist hugs the trees, muting ambient sounds and creating a mystical solitude that feels worlds away from everyday life.
        """
    },
    {
        "slug": "snowy-peaks-expedition",
        "image": "snow-mountain.jpg",
        "author": "Elena Rostova",
        "date": date(2026, 6, 29),
        "title": "Conquering Snow-Covered Mountains",
        "excerpt": "Experience the thrill of high-altitude exploration among pristine glaciers, icy ridges, and frosty winter landscapes.",
        "content": """
        High-altitude expeditions challenge both mind and body, but the vistas from the snowy summit are unequaled. Surrounded by glittering ice fields and untouched snowdrifts, you gain a true appreciation for the majesty of the frozen wilderness.
        
        High-altitude expeditions challenge both mind and body, but the vistas from the snowy summit are unequaled. Surrounded by glittering ice fields and untouched snowdrifts, you gain a true appreciation for the majesty of the frozen wilderness.
        """
    }
]

def short_by_date(post):
    return post["date"]

# Create your views here.
def index(request):
    sorted_post = sorted(posts, key=short_by_date)
    latest = sorted_post[-3:]
    return render(request, "blog/index.html", {
        "latest_post": latest
    })

def blog_grid(request):
    return render(request,"blog/blog-grid.html",{
        "posts": posts
    })
def blog_single(request,slug):
    for single_post in posts:
        if single_post['slug'] == slug :
            return render(request,"blog/blog-single.html",{
                "post": single_post
            })
    return HttpResponse(render_to_string("404.html"))        

 