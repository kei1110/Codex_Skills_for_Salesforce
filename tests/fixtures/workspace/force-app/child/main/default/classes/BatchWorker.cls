public class BatchWorker implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext context) {
        return Database.getQueryLocator('SELECT Id FROM Account');
    }
    public void execute(Database.BatchableContext context, List<SObject> scope) {
    }
    public void finish(Database.BatchableContext context) {
    }
}
