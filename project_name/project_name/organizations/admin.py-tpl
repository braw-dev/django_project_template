from django.contrib import admin

from . import models


@admin.register(models.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "created_at")
    search_fields = ("name", "slug")
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "created_at")
    list_filter = ("organisation",)
    search_fields = ("name", "slug")
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "permissions")
    list_filter = ("organisation",)
    search_fields = ("name",)


@admin.register(models.OrganisationMember)
class OrganisationMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "joined_at")
    list_filter = ("organisation", "role", "joined_at")
    search_fields = ("user__email", "user__username", "organisation__name")
    readonly_fields = ("joined_at",)


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "role", "joined_at")
    list_filter = ("team__organisation", "role", "joined_at")
    search_fields = ("user__email", "user__username", "team__name")
    readonly_fields = ("joined_at",)
