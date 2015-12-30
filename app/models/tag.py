from .. import db


user_tag_association_table = db.Table('user_tag_association',
                                      db.Column('tag_id',
                                                db.Integer,
                                                db.ForeignKey('tags.id')),
                                      db.Column('user_id',
                                                db.Integer,
                                                db.ForeignKey('users.id')))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    users = db.relationship('User',
                            secondary=user_tag_association_table,
                            back_populates='tags')

    @staticmethod
    def find_or_create(name, description=None):
        tag = Tag.query.filter_by(name=name).first()
        if tag is None:
            tag = Tag(name=name, description=description)
            db.session.add(tag)
            db.session.commit()
        return tag

    @staticmethod
    def generate_fake(count=100):
        """Generate a number of fake tags for testing."""
        from faker import Faker

        fake = Faker()
        for i in range(count):
            Tag.find_or_create(fake.word(), description=fake.paragraph())

    def __repr__(self):
        return '<Tag \'%s\'>' % self.name
