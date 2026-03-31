public with sharing class Foo {
    public void run() {
        Bar service = new Bar();
        FooController.load();
        Database.executeBatch(new BatchWorker());
    }
}
