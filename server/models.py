from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    begin = models.DateTimeField()
    end = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    summary = models.TextField(blank=True)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '(%s to %s) at %s' % (self.begin, self.end, self.course)


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.surname, self.first_name)


class Teaching(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return '%s for %s' % (self.teacher, self.course)
