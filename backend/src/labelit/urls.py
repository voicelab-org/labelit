from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r"tasks", views.TaskViewSet)
router.register(r"projects", views.ProjectViewSet, basename="projects")
router.register(
    r"projects_with_stats",
    views.ProjectWithStatsViewSet,
    basename="projects_with_stats",
)
router.register(r"labels", views.LabelViewSet)
router.register(r"annotations", views.AnnotationViewSet)
router.register(r"batches", views.BatchViewSet)
router.register(r"document_sequences", views.DocumentSequenceViewSet)
router.register(r"datasets", views.DatasetViewSet)
router.register(r"lexicons", views.LexiconViewSet)
router.register(r"lexicon_entries", views.LexiconEntryViewSet)
router.register(r"timed_transcripts", views.TimedTranscriptViewSet)
router.register(r"audio", views.AudioViewSet)
router.register(r"export_project", views.ProjectExportViewSet, basename="export")

urlpatterns = [
    path("", include(router.urls)),
    # path('audio/<int:pk>/', views.DownloadAudio.as_view(), name='download_audio_view'),
    # path('audio/<int:pk>/segments/<str:segment_id>', views.DownloadSegment.as_view(), name='download_segment'),
    path("upload_image/", views.ImageUpload.as_view(), name="upload_image_view"),
    path("upload_dataset/", views.DatasetUploadAPI.as_view(), name="upload_dataset"),
    path(
        "download_image/<str:filename>/",
        views.ImageDownload.as_view(),
        name="download_image_view",
    ),
    path("dashboard/", views.StatsView.as_view(), name="dashboard"),
    path("csrf", views.csrf),  # obsolete, todo: remove
]
