import load from '@salesforce/apex/FooController.load';
import helper from 'c/bar';

export default class Foo {
    run() {
        return load().then(() => helper);
    }
}
