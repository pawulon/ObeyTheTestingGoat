from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List
from django.contrib.auth import get_user_model
User = get_user_model()
       
class ItemModelTest(TestCase):
    
    def save_item(self, text, list):
        item = Item()
        item.text = text
        item.list = list
        item.save()        

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
        
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
    
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])
    
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')               
        
    def test_duplicate_items_are_invalid(self):
        duplicate_item_text = 'pompki'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=duplicate_item_text)
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text=duplicate_item_text)
            item.full_clean()
            
    def test_CAN_save_same_item_to_different_lists(self):
        duplicate_item_text = 'pompki'
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text=duplicate_item_text)
        item = Item(list=list2, text=duplicate_item_text)
        item.full_clean()   # should not raise ValidationError
        
class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))
        
    def test_lists_can_have_owners(self):
        user = User.objects.create(email='a@b.com')
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())
        
    def test_list_owner_is_optional(self):
        List.objects.create() # should not raise
        
    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
        
        