import * as cdk from "aws-cdk-lib/core";
import { Function, Runtime, Code } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import path from "path";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class PyAgentStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lambda = new Function(this, "python-lambda", {
      runtime: Runtime.PYTHON_3_12,
      handler: "agentLambda.agent.handler",
      code: Code.fromAsset("src/lambdas/lambda_package.zip"),
    });
    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'PyAgentQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
