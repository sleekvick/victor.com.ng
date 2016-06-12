'use strict';

class Person {

    constructor (name, role) {
        this.name = name;
        this.role = role;
    }

    greet () {
        return `Hello my name is ${this.name} i am a ${this.role}`;
    }

}

sleekvick = new Person("Victor Nwaokocha", "Software Developer");

console.log(sleekvick.greet());
