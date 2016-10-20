from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List
       
class ListAndItemModelTest(TestCase):
    
    def save_item(self, text, list):
        item = Item()
        item.text = text
        item.list = list
        item.save()        
        
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        self.save_item('The first (ever) list item', list_)
        self.save_item('Item the second', list_)
        
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
    
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
            
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))