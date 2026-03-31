trigger AccountTrigger on Account (after insert) {
    AccountTriggerHandler.handle(Trigger.new);
}
