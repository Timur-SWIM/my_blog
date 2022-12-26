from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):  #Форма входа пользователя
    username = StringField('Логин', validators=[DataRequired()]) #Валидатор DataRequired проверяет 
    password = PasswordField('Пароль', validators=[DataRequired()]) #что поле не отправлено пустым
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class RegistrationForm(FlaskForm): #Форма регистрации пользователя
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    status = StringField('Статус',validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        '''Функция проверки логина''' 
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалйста используйте другой логин.')

    def validate_email(self, email):
        '''Функция проверки почты''' 
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалйста используйте другую почту.')


class EditProfileForm(FlaskForm):    #Форма редактирования профиля пользователя
    username = StringField('Логин', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Подтвердить')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Пожалуйста используйте другой логин.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Подтвердить')


class PostForm(FlaskForm):     # Форма создвния поста
    post = TextAreaField('Весь университет ждет ваших постов!', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
