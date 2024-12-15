from app.modules.dataset.models import DataSet
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.modules.profile import profile_bp
from app.modules.profile.forms import UserProfileForm
from app.modules.profile.services import UserProfileService


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    profile = current_user.profile
    if not profile:
        return redirect(url_for("public.index"))

    form = UserProfileForm()
    if request.method == "POST":
        service = UserProfileService()
        try:
            service.update_profile(profile.id, form)
            return redirect(url_for("profile.my_profile"))  # Redirige a la página de usuario

        except Exception as exc:
            return render_template("profile/edit.html", form=form, error=f"Error updating profile: {exc}")

    return render_template("profile/edit.html", form=form)


@profile_bp.route('/profile/summary')
@login_required
def my_profile():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    user_datasets_pagination = db.session.query(DataSet) \
        .filter(DataSet.user_id == current_user.id) \
        .order_by(DataSet.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    total_datasets_count = db.session.query(DataSet) \
        .filter(DataSet.user_id == current_user.id) \
        .count()

    print(user_datasets_pagination.items)

    return render_template(
        'profile/summary.html',
        user_profile=current_user.profile,
        user=current_user,
        datasets=user_datasets_pagination.items,
        pagination=user_datasets_pagination,
        total_datasets=total_datasets_count,
        developer=current_user.profile.user.developer
    )
